#!/usr/bin/env node
/**
 * scripts/gen_stress_test.js
 *
 * Generates examples/stress_test.cat — a 10,000-line valid CAT source file
 * used for benchmarking the lexer. Covers all token types across the file
 * to give realistic benchmark numbers.
 */

const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '..', 'examples', 'stress_test.cat');

const lines = [];

lines.push('# Auto-generated stress test — 10,000 lines of valid CAT');
lines.push('# Do not edit by hand. Regenerate with: node scripts/gen_stress_test.js');
lines.push('');

const TYPES   = ['i8','i16','i32','i64','u8','u16','u32','u64','f32','f64','bool'];
const INSTR   = ['add','sub','mul','div','mod','and','orr','xor','shl','shr'];
const KWS     = ['local','global','const'];
const DIRS    = ['@inline','@static','@packed','@align(8)'];

// Generate 9800 simple functions + data (mix of patterns)
for (let i = 0; i < 4900; i++) {
    const ty  = TYPES[i % TYPES.length];
    const ins = INSTR[i % INSTR.length];
    const kw  = KWS[i % KWS.length];
    const dir = DIRS[i % DIRS.length];

    lines.push(`# Function ${i}: type=${ty} op=${ins}`);
    lines.push(`${dir}`);
    lines.push(`fn func_${i}(a: ${ty}, b: ${ty}) -> ${ty} {`);
    lines.push(`    ${kw} result: ${ty} = 0`);
    lines.push(`    ${ins} result, a, b`);
    lines.push(`    ret result`);
    lines.push(`}`);
    lines.push('');
}

// Generate 50 struct definitions
for (let i = 0; i < 50; i++) {
    lines.push(`type Vec${i} {`);
    lines.push(`    x: f32`);
    lines.push(`    y: f32`);
    lines.push(`    z: f32`);
    lines.push(`    w: f32`);
    lines.push(`}`);
    lines.push('');
}

// Generate 50 enum definitions
for (let i = 0; i < 50; i++) {
    lines.push(`type Result${i} = enum {`);
    lines.push(`    Ok(value: i32)`);
    lines.push(`    Err(code: u32)`);
    lines.push(`}`);
    lines.push('');
}

// Entry point
lines.push('fn main() -> i32 {');
lines.push('    local sum: i64 = 0');
for (let i = 0; i < 20; i++) {
    const ty = TYPES[i % TYPES.length];
    lines.push(`    local v${i}: ${ty} = ${i}`);
}
lines.push('    ret 0');
lines.push('}');

const content = lines.join('\n');
fs.writeFileSync(OUT, content, 'utf8');

const lineCount = content.split('\n').length;
const byteCount = Buffer.byteLength(content, 'utf8');
console.log(`Generated: ${OUT}`);
console.log(`  Lines:   ${lineCount.toLocaleString()}`);
console.log(`  Bytes:   ${byteCount.toLocaleString()}`);
