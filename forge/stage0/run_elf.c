/* C test harness: load a Forge-compiled ELF binary and run it */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s <elf_binary>\n", argv[0]); return 1; }
    
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) { perror("open"); return 1; }
    
    struct stat st;
    fstat(fd, &st);
    size_t size = st.st_size;
    
    uint8_t* data = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    if (data == MAP_FAILED) { perror("mmap"); return 1; }
    
    /* Parse ELF header */
    if (data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
        fprintf(stderr, "not an ELF\n"); return 1;
    }
    if (data[4] != 2) { fprintf(stderr, "not 64-bit\n"); return 1; }
    
    uint64_t entry = *(uint64_t*)(data + 24);
    uint64_t phoff = *(uint64_t*)(data + 32);
    uint16_t phnum = *(uint16_t*)(data + 56);
    uint16_t phentsize = *(uint16_t*)(data + 54);
    
    /* Find PT_LOAD segment */
    uint64_t code_vaddr = 0, code_size = 0, code_offset = 0, code_flags = 0;
    for (int i = 0; i < phnum; i++) {
        uint8_t* ph = data + phoff + i * phentsize;
        uint32_t p_type = *(uint32_t*)ph;
        if (p_type == 1) { /* PT_LOAD */
            code_offset = *(uint64_t*)(ph + 8);
            code_vaddr = *(uint64_t*)(ph + 16);
            code_size = *(uint64_t*)(ph + 32);
            code_flags = *(uint32_t*)(ph + 4);
            break;
        }
    }
    
    if (code_size == 0) { fprintf(stderr, "no PT_LOAD\n"); return 1; }
    if (code_offset + code_size > size) code_size = size - code_offset;
    
    /* Copy code to a temp file, then mmap with exec */
    char tmpname[] = "/tmp/forge_code_XXXXXX";
    int tmpfd = mkstemp(tmpname);
    if (tmpfd < 0) { perror("mkstemp"); return 1; }
    unlink(tmpname);
    
    /* Extend file to code_size */
    ftruncate(tmpfd, code_size);
    
    /* Write code */
    write(tmpfd, data + code_offset, code_size);
    
    /* Mmap with exec */
    void* mapped = mmap(NULL, code_size, PROT_READ | PROT_EXEC,
                        MAP_PRIVATE, tmpfd, 0);
    close(tmpfd);
    if (mapped == MAP_FAILED) { perror("mmap exec"); return 1; }
    
    munmap(data, size);
    
    /* Entry offset within the code */
    uint64_t entry_off = entry - code_vaddr;
    if (entry_off >= code_size) { fprintf(stderr, "entry outside code\n"); return 1; }
    
    /* Call entry */
    fprintf(stderr, "calling entry at offset 0x%llx in code...\n", (unsigned long long)entry_off);
    int (*fn)(void) = (int (*)(void))((uintptr_t)mapped + entry_off);
    int result = fn();
    fprintf(stderr, "returned: %d\n", result);
    
    munmap(mapped, code_size);
    return result;
}
