`timescale 1ns / 1ps

module svm (
    input wire clk,
    // Weights a0 to a311
    input wire signed [31:0] a0, a1, a2, a3, a4, a5, a6, a7, a8, a9,
    input wire signed [31:0] a10, a11, a12, a13, a14, a15, a16, a17, a18, a19,
    input wire signed [31:0] a20, a21, a22, a23, a24, a25, a26, a27, a28, a29,
    input wire signed [31:0] a30, a31, a32, a33, a34, a35, a36, a37, a38, a39,
    input wire signed [31:0] a40, a41, a42, a43, a44, a45, a46, a47, a48, a49,
    input wire signed [31:0] a50, a51, a52, a53, a54, a55, a56, a57, a58, a59,
    input wire signed [31:0] a60, a61, a62, a63, a64, a65, a66, a67, a68, a69,
    input wire signed [31:0] a70, a71, a72, a73, a74, a75, a76, a77, a78, a79,
    input wire signed [31:0] a80, a81, a82, a83, a84, a85, a86, a87, a88, a89,
    input wire signed [31:0] a90, a91, a92, a93, a94, a95, a96, a97, a98, a99,
    input wire signed [31:0] a100, a101, a102, a103, a104, a105, a106, a107, a108, a109,
    input wire signed [31:0] a110, a111, a112, a113, a114, a115, a116, a117, a118, a119,
    input wire signed [31:0] a120, a121, a122, a123, a124, a125, a126, a127, a128, a129,
    input wire signed [31:0] a130, a131, a132, a133, a134, a135, a136, a137, a138, a139,
    input wire signed [31:0] a140, a141, a142, a143, a144, a145, a146, a147, a148, a149,
    input wire signed [31:0] a150, a151, a152, a153, a154, a155, a156, a157, a158, a159,
    input wire signed [31:0] a160, a161, a162, a163, a164, a165, a166, a167, a168, a169,
    input wire signed [31:0] a170, a171, a172, a173, a174, a175, a176, a177, a178, a179,
    input wire signed [31:0] a180, a181, a182, a183, a184, a185, a186, a187, a188, a189,
    input wire signed [31:0] a190, a191, a192, a193, a194, a195, a196, a197, a198, a199,
    input wire signed [31:0] a200, a201, a202, a203, a204, a205, a206, a207, a208, a209,
    input wire signed [31:0] a210, a211, a212, a213, a214, a215, a216, a217, a218, a219,
    input wire signed [31:0] a220, a221, a222, a223, a224, a225, a226, a227, a228, a229,
    input wire signed [31:0] a230, a231, a232, a233, a234, a235, a236, a237, a238, a239,
    input wire signed [31:0] a240, a241, a242, a243, a244, a245, a246, a247, a248, a249,
    input wire signed [31:0] a250, a251, a252, a253, a254, a255, a256, a257, a258, a259,
    input wire signed [31:0] a260, a261, a262, a263, a264, a265, a266, a267, a268, a269,
    input wire signed [31:0] a270, a271, a272, a273, a274, a275, a276, a277, a278, a279,
    input wire signed [31:0] a280, a281, a282, a283, a284, a285, a286, a287, a288, a289,
    input wire signed [31:0] a290, a291, a292, a293, a294, a295, a296, a297, a298, a299,
    input wire signed [31:0] a300, a301, a302, a303, a304, a305, a306, a307, a308, a309,
    input wire signed [31:0] a310, a311,
    
    // Input features x0 to x311
    input wire signed [31:0] x0, x1, x2, x3, x4, x5, x6, x7, x8, x9,
    input wire signed [31:0] x10, x11, x12, x13, x14, x15, x16, x17, x18, x19,
    input wire signed [31:0] x20, x21, x22, x23, x24, x25, x26, x27, x28, x29,
    input wire signed [31:0] x30, x31, x32, x33, x34, x35, x36, x37, x38, x39,
    input wire signed [31:0] x40, x41, x42, x43, x44, x45, x46, x47, x48, x49,
    input wire signed [31:0] x50, x51, x52, x53, x54, x55, x56, x57, x58, x59,
    input wire signed [31:0] x60, x61, x62, x63, x64, x65, x66, x67, x68, x69,
    input wire signed [31:0] x70, x71, x72, x73, x74, x75, x76, x77, x78, x79,
    input wire signed [31:0] x80, x81, x82, x83, x84, x85, x86, x87, x88, x89,
    input wire signed [31:0] x90, x91, x92, x93, x94, x95, x96, x97, x98, x99,
    input wire signed [31:0] x100, x101, x102, x103, x104, x105, x106, x107, x108, x109,
    input wire signed [31:0] x110, x111, x112, x113, x114, x115, x116, x117, x118, x119,
    input wire signed [31:0] x120, x121, x122, x123, x124, x125, x126, x127, x128, x129,
    input wire signed [31:0] x130, x131, x132, x133, x134, x135, x136, x137, x138, x139,
    input wire signed [31:0] x140, x141, x142, x143, x144, x145, x146, x147, x148, x149,
    input wire signed [31:0] x150, x151, x152, x153, x154, x155, x156, x157, x158, x159,
    input wire signed [31:0] x160, x161, x162, x163, x164, x165, x166, x167, x168, x169,
    input wire signed [31:0] x170, x171, x172, x173, x174, x175, x176, x177, x178, x179,
    input wire signed [31:0] x180, x181, x182, x183, x184, x185, x186, x187, x188, x189,
    input wire signed [31:0] x190, x191, x192, x193, x194, x195, x196, x197, x198, x199,
    input wire signed [31:0] x200, x201, x202, x203, x204, x205, x206, x207, x208, x209,
    input wire signed [31:0] x210, x211, x212, x213, x214, x215, x216, x217, x218, x219,
    input wire signed [31:0] x220, x221, x222, x223, x224, x225, x226, x227, x228, x229,
    input wire signed [31:0] x230, x231, x232, x233, x234, x235, x236, x237, x238, x239,
    input wire signed [31:0] x240, x241, x242, x243, x244, x245, x246, x247, x248, x249,
    input wire signed [31:0] x250, x251, x252, x253, x254, x255, x256, x257, x258, x259,
    input wire signed [31:0] x260, x261, x262, x263, x264, x265, x266, x267, x268, x269,
    input wire signed [31:0] x270, x271, x272, x273, x274, x275, x276, x277, x278, x279,
    input wire signed [31:0] x280, x281, x282, x283, x284, x285, x286, x287, x288, x289,
    input wire signed [31:0] x290, x291, x292, x293, x294, x295, x296, x297, x298, x299,
    input wire signed [31:0] x300, x301, x302, x303, x304, x305, x306, x307, x308, x309,
    input wire signed [31:0] x310, x311,
    
    output reg signed [63:0] y
);

    // Internal registers for partial sums to improve timing
    reg signed [63:0] sum_0_77;    // Sum for inputs 0-77
    reg signed [63:0] sum_78_155;  // Sum for inputs 78-155
    reg signed [63:0] sum_156_233; // Sum for inputs 156-233
    reg signed [63:0] sum_234_311; // Sum for inputs 234-311

    // Pipeline register for final sum
    reg signed [63:0] final_sum;

    always @(posedge clk) begin
        // First stage: Calculate partial sums
        
        // First quarter (0-77)
        sum_0_77 <= (a0 * x0) + (a1 * x1) + (a2 * x2) + (a3 * x3) + (a4 * x4) +
                    (a5 * x5) + (a6 * x6) + (a7 * x7) + (a8 * x8) + (a9 * x9) +
                    (a10 * x10) + (a11 * x11) + (a12 * x12) + (a13 * x13) + (a14 * x14) +
                    (a15 * x15) + (a16 * x16) + (a17 * x17) + (a18 * x18) + (a19 * x19) +
                    (a20 * x20) + (a21 * x21) + (a22 * x22) + (a23 * x23) + (a24 * x24) +
                    (a25 * x25) + (a26 * x26) + (a27 * x27) + (a28 * x28) + (a29 * x29) +
                    (a30 * x30) + (a31 * x31) + (a32 * x32) + (a33 * x33) + (a34 * x34) +
                    (a35 * x35) + (a36 * x36) + (a37 * x37) + (a38 * x38) + (a39 * x39) +
                    (a40 * x40) + (a41 * x41) + (a42 * x42) + (a43 * x43) + (a44 * x44) +
                    (a45 * x45) + (a46 * x46) + (a47 * x47) + (a48 * x48) + (a49 * x49) +
                    (a50 * x50) + (a51 * x51) + (a52 * x52) + (a53 * x53) + (a54 * x54) +
                    (a55 * x55) + (a56 * x56) + (a57 * x57) + (a58 * x58) + (a59 * x59) +
                    (a60 * x60) + (a61 * x61) + (a62 * x62) + (a63 * x63) + (a64 * x64) +
                    (a65 * x65) + (a66 * x66) + (a67 * x67) + (a68 * x68) + (a69 * x69) +
                    (a70 * x70) + (a71 * x71) + (a72 * x72) + (a73 * x73) + (a74 * x74) +
                    (a75 * x75) +
                    (a76 * x76) + (a77 * x77);

        // Second quarter (78-155)
        sum_78_155 <= (a78 * x78) + (a79 * x79) + (a80 * x80) + (a81 * x81) + (a82 * x82) +
                      (a83 * x83) + (a84 * x84) + (a85 * x85) + (a86 * x86) + (a87 * x87) +
                    (a88 * x88) + (a89 * x89) + (a90 * x90) + (a91 * x91) + (a92 * x92) +
                    (a93 * x93) + (a94 * x94) + (a95 * x95) + (a96 * x96) + (a97 * x97) +
                    (a98 * x98) + (a99 * x99) + (a100 * x100) + (a101 * x101) + (a102 * x102) +
                    (a103 * x103) + (a104 * x104) + (a105 * x105) + (a106 * x106) + (a107 * x107) +
                    (a108 * x108) + (a109 * x109) + (a110 * x110) + (a111 * x111) + (a112 * x112) +
                    (a113 * x113) + (a114 * x114) + (a115 * x115) + (a116 * x116) + (a117 * x117) +
                    (a118 * x118) + (a119 * x119) + (a120 * x120) + (a121 * x121) + (a122 * x122) +
                    (a123 * x123) + (a124 * x124) + (a125 * x125) + (a126 * x126) + (a127 * x127) +
                    (a128 * x128) + (a129 * x129) + (a130 * x130) + (a131 * x131) + (a132 * x132) +
                    (a133 * x133) + (a134 * x134) + (a135 * x135) + (a136 * x136) + (a137 * x137) +
                    (a138 * x138) + (a139 * x139) + (a140 * x140) + (a141 * x141) + (a142 * x142) +
                    (a143 * x143) + (a144 * x144) + (a145 * x145) + (a146 * x146) + (a147 * x147) +
                    (a148 * x148) + (a149 * x149) + (a150 * x150) + (a151 * x151) + (a152 * x152) +
                    (a153 * x153) +
                      (a154 * x154) + (a155 * x155);

        // Third quarter (156-233)
        sum_156_233 <= (a156 * x156) + (a157 * x157) + (a158 * x158) + (a159 * x159) +
                       (a160 * x160) + (a161 * x161) + (a162 * x162) + (a163 * x163) +
                    (a164 * x164) + (a165 * x165) + (a166 * x166) + (a167 * x167) + (a168 * x168) +
                    (a169 * x169) + (a170 * x170) + (a171 * x171) + (a172 * x172) + (a173 * x173) +
                    (a174 * x174) + (a175 * x175) + (a176 * x176) + (a177 * x177) + (a178 * x178) +
                    (a179 * x179) + (a180 * x180) + (a181 * x181) + (a182 * x182) + (a183 * x183) +
                    (a184 * x184) + (a185 * x185) + (a186 * x186) + (a187 * x187) + (a188 * x188) +
                    (a189 * x189) + (a190 * x190) + (a191 * x191) + (a192 * x192) + (a193 * x193) +
                    (a194 * x194) + (a195 * x195) + (a196 * x196) + (a197 * x197) + (a198 * x198) +
                    (a199 * x199) + (a200 * x200) + (a201 * x201) + (a202 * x202) + (a203 * x203) +
                    (a204 * x204) + (a205 * x205) + (a206 * x206) + (a207 * x207) + (a208 * x208) +
                    (a209 * x209) + (a210 * x210) + (a211 * x211) + (a212 * x212) + (a213 * x213) +
                    (a214 * x214) + (a215 * x215) + (a216 * x216) + (a217 * x217) + (a218 * x218) +
                    (a219 * x219) + (a220 * x220) + (a221 * x221) + (a222 * x222) + (a223 * x223) +
                    (a224 * x224) + (a225 * x225) + (a226 * x226) + (a227 * x227) + (a228 * x228) +
                    (a229 * x229) + (a230 * x230) + (a231 * x231) +
                       (a232 * x232) + (a233 * x233);

        // Fourth quarter (234-311)
        sum_234_311 <= (a234 * x234) + (a235 * x235) + (a236 * x236) + (a237 * x237) +
                       (a238 * x238) + (a239 * x239) + (a240 * x240) + (a241 * x241) +
                    (a242 * x242) + (a243 * x243) + (a244 * x244) + (a245 * x245) + (a246 * x246) +
                    (a247 * x247) + (a248 * x248) + (a249 * x249) + (a250 * x250) + (a251 * x251) +
                    (a252 * x252) + (a253 * x253) + (a254 * x254) + (a255 * x255) + (a256 * x256) +
                    (a257 * x257) + (a258 * x258) + (a259 * x259) + (a260 * x260) + (a261 * x261) +
                    (a262 * x262) + (a263 * x263) + (a264 * x264) + (a265 * x265) + (a266 * x266) +
                    (a267 * x267) + (a268 * x268) + (a269 * x269) + (a270 * x270) + (a271 * x271) +
                    (a272 * x272) + (a273 * x273) + (a274 * x274) + (a275 * x275) + (a276 * x276) +
                    (a277 * x277) + (a278 * x278) + (a279 * x279) + (a280 * x280) + (a281 * x281) +
                    (a282 * x282) + (a283 * x283) + (a284 * x284) + (a285 * x285) + (a286 * x286) +
                    (a287 * x287) + (a288 * x288) + (a289 * x289) + (a290 * x290) + (a291 * x291) +
                    (a292 * x292) + (a293 * x293) + (a294 * x294) + (a295 * x295) + (a296 * x296) +
                    (a297 * x297) + (a298 * x298) + (a299 * x299) + (a300 * x300) + (a301 * x301) +
                    (a302 * x302) + (a303 * x303) + (a304 * x304) + (a305 * x305) + (a306 * x306) +
                    (a307 * x307) + (a308 * x308) + (a309 * x309) +
                       (a310 * x310) + (a311 * x311);
                       
        // Second stage: Combine partial sums
        final_sum <= sum_0_77 + sum_78_155 + sum_156_233 + sum_234_311;
        
        // Final stage: Output register
        y <= final_sum;
    end

endmodule