`timescale 1ns/1ps

module svm_testbench;

    // Clock
    reg clk = 0;
    always #10 clk = ~clk;  // 50MHz clock

    // We'll assume we have 10 inputs/weights for the new SVM module
    // (Matching the new `svm_10` definition)
    reg signed [31:0] a0, a1, a2, a3, a4, a5, a6, a7, a8, a9;
    reg signed [31:0] a10, a11, a12, a13, a14, a15, a16, a17, a18, a19;
    reg signed [31:0] a20, a21, a22, a23, a24, a25, a26, a27, a28, a29;
    reg signed [31:0] a30, a31;
    reg signed [31:0] a32, a33, a34, a35, a36, a37, a38, a39, a40, a41;
    reg signed [31:0] a42, a43, a44, a45, a46, a47, a48, a49, a50, a51;
    reg signed [31:0] a52, a53, a54, a55, a56, a57, a58, a59, a60, a61;
    reg signed [31:0] a62, a63, a64, a65, a66, a67, a68, a69, a70, a71;
    reg signed [31:0] a72, a73, a74, a75, a76, a77, a78, a79, a80, a81;
    reg signed [31:0] a82, a83, a84, a85, a86, a87, a88, a89, a90, a91;
    reg signed [31:0] a92, a93, a94, a95, a96, a97, a98, a99, a100, a101;
    reg signed [31:0] a102, a103, a104, a105, a106, a107, a108, a109, a110, a111;
    reg signed [31:0] a112, a113, a114, a115, a116, a117, a118, a119, a120, a121;
    reg signed [31:0] a122, a123, a124, a125, a126, a127, a128, a129, a130, a131;
    reg signed [31:0] a132, a133, a134, a135, a136, a137, a138, a139, a140, a141;
    reg signed [31:0] a142, a143, a144, a145, a146, a147, a148, a149, a150, a151;
    reg signed [31:0] a152, a153, a154, a155, a156, a157, a158, a159, a160, a161;
    reg signed [31:0] a162, a163, a164, a165, a166, a167, a168, a169, a170, a171;
    reg signed [31:0] a172, a173, a174, a175, a176, a177, a178, a179, a180, a181;
    reg signed [31:0] a182, a183, a184, a185, a186, a187, a188, a189, a190, a191;
    reg signed [31:0] a192, a193, a194, a195, a196, a197, a198, a199, a200, a201;
    reg signed [31:0] a202, a203, a204, a205, a206, a207, a208, a209, a210, a211;
    reg signed [31:0] a212, a213, a214, a215, a216, a217, a218, a219, a220, a221;
    reg signed [31:0] a222, a223, a224, a225, a226, a227, a228, a229, a230, a231;
    reg signed [31:0] a232, a233, a234, a235, a236, a237, a238, a239, a240, a241;
    reg signed [31:0] a242, a243, a244, a245, a246, a247, a248, a249, a250, a251;
    reg signed [31:0] a252, a253, a254, a255, a256, a257, a258, a259, a260, a261;
    reg signed [31:0] a262, a263, a264, a265, a266, a267, a268, a269, a270, a271;
    reg signed [31:0] a272, a273, a274, a275, a276, a277, a278, a279, a280, a281;
    reg signed [31:0] a282, a283, a284, a285, a286, a287, a288, a289, a290, a291;
    reg signed [31:0] a292, a293, a294, a295, a296, a297, a298, a299, a300, a301;
    reg signed [31:0] a302, a303, a304, a305, a306, a307, a308, a309, a310, a311;

    reg signed [31:0] x0, x1, x2, x3, x4, x5, x6, x7, x8, x9;
    reg signed [31:0] x10, x11, x12, x13, x14, x15, x16, x17, x18, x19;
    reg signed [31:0] x20, x21, x22, x23, x24, x25, x26, x27, x28, x29;
    reg signed [31:0] x30, x31;
    reg signed [31:0] x32, x33, x34, x35, x36, x37, x38, x39, x40, x41;
    reg signed [31:0] x42, x43, x44, x45, x46, x47, x48, x49, x50, x51;
    reg signed [31:0] x52, x53, x54, x55, x56, x57, x58, x59, x60, x61;
    reg signed [31:0] x62, x63, x64, x65, x66, x67, x68, x69, x70, x71;
    reg signed [31:0] x72, x73, x74, x75, x76, x77, x78, x79, x80, x81;
    reg signed [31:0] x82, x83, x84, x85, x86, x87, x88, x89, x90, x91;
    reg signed [31:0] x92, x93, x94, x95, x96, x97, x98, x99, x100, x101;
    reg signed [31:0] x102, x103, x104, x105, x106, x107, x108, x109, x110, x111;
    reg signed [31:0] x112, x113, x114, x115, x116, x117, x118, x119, x120, x121;
    reg signed [31:0] x122, x123, x124, x125, x126, x127, x128, x129, x130, x131;
    reg signed [31:0] x132, x133, x134, x135, x136, x137, x138, x139, x140, x141;
    reg signed [31:0] x142, x143, x144, x145, x146, x147, x148, x149, x150, x151;
    reg signed [31:0] x152, x153, x154, x155, x156, x157, x158, x159, x160, x161;
    reg signed [31:0] x162, x163, x164, x165, x166, x167, x168, x169, x170, x171;
    reg signed [31:0] x172, x173, x174, x175, x176, x177, x178, x179, x180, x181;
    reg signed [31:0] x182, x183, x184, x185, x186, x187, x188, x189, x190, x191;
    reg signed [31:0] x192, x193, x194, x195, x196, x197, x198, x199, x200, x201;
    reg signed [31:0] x202, x203, x204, x205, x206, x207, x208, x209, x210, x211;
    reg signed [31:0] x212, x213, x214, x215, x216, x217, x218, x219, x220, x221;
    reg signed [31:0] x222, x223, x224, x225, x226, x227, x228, x229, x230, x231;
    reg signed [31:0] x232, x233, x234, x235, x236, x237, x238, x239, x240, x241;
    reg signed [31:0] x242, x243, x244, x245, x246, x247, x248, x249, x250, x251;
    reg signed [31:0] x252, x253, x254, x255, x256, x257, x258, x259, x260, x261;
    reg signed [31:0] x262, x263, x264, x265, x266, x267, x268, x269, x270, x271;
    reg signed [31:0] x272, x273, x274, x275, x276, x277, x278, x279, x280, x281;
    reg signed [31:0] x282, x283, x284, x285, x286, x287, x288, x289, x290, x291;
    reg signed [31:0] x292, x293, x294, x295, x296, x297, x298, x299, x300, x301;
    reg signed [31:0] x302, x303, x304, x305, x306, x307, x308, x309, x310, x311;
    wire signed [63:0] y;

    // Arrays for file reading
    reg [31:0] input_data   [0:311];
    reg [31:0] weights_data [0:311];

    // File handling
    integer buffer_in, buffer_weights, buffer_out;
    integer r, i;

    // Instantiate the new SVM module
    svm svm_inst (
        .clk(clk),
        .a0(a0), .a1(a1), .a2(a2), .a3(a3), .a4(a4),
        .a5(a5), .a6(a6), .a7(a7), .a8(a8), .a9(a9),
        .a10(a10), .a11(a11), .a12(a12), .a13(a13), .a14(a14),
        .a15(a15), .a16(a16), .a17(a17), .a18(a18), .a19(a19),
        .a20(a20), .a21(a21), .a22(a22), .a23(a23), .a24(a24),
        .a25(a25), .a26(a26), .a27(a27), .a28(a28), .a29(a29),
        .a30(a30), .a31(a31), .a32(a32), .a33(a33), .a34(a34),
        .a35(a35), .a36(a36), .a37(a37), .a38(a38), .a39(a39),
        .a40(a40), .a41(a41), .a42(a42), .a43(a43), .a44(a44),
        .a45(a45), .a46(a46), .a47(a47), .a48(a48), .a49(a49),
        .a50(a50), .a51(a51), .a52(a52), .a53(a53), .a54(a54),
        .a55(a55), .a56(a56), .a57(a57), .a58(a58), .a59(a59),
        .a60(a60), .a61(a61), .a62(a62), .a63(a63), .a64(a64),
        .a65(a65), .a66(a66), .a67(a67), .a68(a68), .a69(a69),
        .a70(a70), .a71(a71), .a72(a72), .a73(a73), .a74(a74),
        .a75(a75), .a76(a76), .a77(a77), .a78(a78), .a79(a79),
        .a80(a80), .a81(a81), .a82(a82), .a83(a83), .a84(a84),
        .a85(a85), .a86(a86), .a87(a87), .a88(a88), .a89(a89),
        .a90(a90), .a91(a91), .a92(a92), .a93(a93), .a94(a94),
        .a95(a95), .a96(a96), .a97(a97), .a98(a98), .a99(a99),
        .a100(a100), .a101(a101), .a102(a102), .a103(a103), .a104(a104),
        .a105(a105), .a106(a106), .a107(a107), .a108(a108), .a109(a109),
        .a110(a110), .a111(a111), .a112(a112), .a113(a113), .a114(a114),
        .a115(a115), .a116(a116), .a117(a117), .a118(a118), .a119(a119),
        .a120(a120), .a121(a121), .a122(a122), .a123(a123), .a124(a124),
        .a125(a125), .a126(a126), .a127(a127), .a128(a128), .a129(a129),
        .a130(a130), .a131(a131), .a132(a132), .a133(a133), .a134(a134),
        .a135(a135), .a136(a136), .a137(a137), .a138(a138), .a139(a139),
        .a140(a140), .a141(a141), .a142(a142), .a143(a143), .a144(a144),
        .a145(a145), .a146(a146), .a147(a147), .a148(a148), .a149(a149),
        .a150(a150), .a151(a151), .a152(a152), .a153(a153), .a154(a154),
        .a155(a155), .a156(a156), .a157(a157), .a158(a158), .a159(a159),
        .a160(a160), .a161(a161), .a162(a162), .a163(a163), .a164(a164),
        .a165(a165), .a166(a166), .a167(a167), .a168(a168), .a169(a169),
        .a170(a170), .a171(a171), .a172(a172), .a173(a173), .a174(a174),
        .a175(a175), .a176(a176), .a177(a177), .a178(a178), .a179(a179),
        .a180(a180), .a181(a181), .a182(a182), .a183(a183), .a184(a184),
        .a185(a185), .a186(a186), .a187(a187), .a188(a188), .a189(a189),
        .a190(a190), .a191(a191), .a192(a192), .a193(a193), .a194(a194),
        .a195(a195), .a196(a196), .a197(a197), .a198(a198), .a199(a199),
        .a200(a200), .a201(a201), .a202(a202), .a203(a203), .a204(a204),
        .a205(a205), .a206(a206), .a207(a207), .a208(a208), .a209(a209),
        .a210(a210), .a211(a211), .a212(a212), .a213(a213), .a214(a214),
        .a215(a215), .a216(a216), .a217(a217), .a218(a218), .a219(a219),
        .a220(a220), .a221(a221), .a222(a222), .a223(a223), .a224(a224),
        .a225(a225), .a226(a226), .a227(a227), .a228(a228), .a229(a229),
        .a230(a230), .a231(a231), .a232(a232), .a233(a233), .a234(a234),
        .a235(a235), .a236(a236), .a237(a237), .a238(a238), .a239(a239),
        .a240(a240), .a241(a241), .a242(a242), .a243(a243), .a244(a244),
        .a245(a245), .a246(a246), .a247(a247), .a248(a248), .a249(a249),
        .a250(a250), .a251(a251), .a252(a252), .a253(a253), .a254(a254),
        .a255(a255), .a256(a256), .a257(a257), .a258(a258), .a259(a259),
        .a260(a260), .a261(a261), .a262(a262), .a263(a263), .a264(a264),
        .a265(a265), .a266(a266), .a267(a267), .a268(a268), .a269(a269),
        .a270(a270), .a271(a271), .a272(a272), .a273(a273), .a274(a274),
        .a275(a275), .a276(a276), .a277(a277), .a278(a278), .a279(a279),
        .a280(a280), .a281(a281), .a282(a282), .a283(a283), .a284(a284),
        .a285(a285), .a286(a286), .a287(a287), .a288(a288), .a289(a289),
        .a290(a290), .a291(a291), .a292(a292), .a293(a293), .a294(a294),
        .a295(a295), .a296(a296), .a297(a297), .a298(a298), .a299(a299),
        .a300(a300), .a301(a301), .a302(a302), .a303(a303), .a304(a304),
        .a305(a305), .a306(a306), .a307(a307), .a308(a308), .a309(a309),
        .a310(a310), .a311(a311),
        .x0(x0), .x1(x1), .x2(x2), .x3(x3), .x4(x4),
        .x5(x5), .x6(x6), .x7(x7), .x8(x8), .x9(x9),
        .x10(x10), .x11(x11), .x12(x12), .x13(x13), .x14(x14),
        .x15(x15), .x16(x16), .x17(x17), .x18(x18), .x19(x19),
        .x20(x20), .x21(x21), .x22(x22), .x23(x23), .x24(x24),
        .x25(x25), .x26(x26), .x27(x27), .x28(x28), .x29(x29),
        .x30(x30), .x31(x31), .x32(x32), .x33(x33), .x34(x34),
        .x35(x35), .x36(x36), .x37(x37), .x38(x38), .x39(x39),
        .x40(x40), .x41(x41), .x42(x42), .x43(x43), .x44(x44),
        .x45(x45), .x46(x46), .x47(x47), .x48(x48), .x49(x49),
        .x50(x50), .x51(x51), .x52(x52), .x53(x53), .x54(x54),
        .x55(x55), .x56(x56), .x57(x57), .x58(x58), .x59(x59),
        .x60(x60), .x61(x61), .x62(x62), .x63(x63), .x64(x64),
        .x65(x65), .x66(x66), .x67(x67), .x68(x68), .x69(x69),
        .x70(x70), .x71(x71), .x72(x72), .x73(x73), .x74(x74),
        .x75(x75), .x76(x76), .x77(x77), .x78(x78), .x79(x79),
        .x80(x80), .x81(x81), .x82(x82), .x83(x83), .x84(x84),
        .x85(x85), .x86(x86), .x87(x87), .x88(x88), .x89(x89),
        .x90(x90), .x91(x91), .x92(x92), .x93(x93), .x94(x94),
        .x95(x95), .x96(x96), .x97(x97), .x98(x98), .x99(x99),
        .x100(x100), .x101(x101), .x102(x102), .x103(x103), .x104(x104),
        .x105(x105), .x106(x106), .x107(x107), .x108(x108), .x109(x109),
        .x110(x110), .x111(x111), .x112(x112), .x113(x113), .x114(x114),
        .x115(x115), .x116(x116), .x117(x117), .x118(x118), .x119(x119),
        .x120(x120), .x121(x121), .x122(x122), .x123(x123), .x124(x124),
        .x125(x125), .x126(x126), .x127(x127), .x128(x128), .x129(x129),
        .x130(x130), .x131(x131), .x132(x132), .x133(x133), .x134(x134),
        .x135(x135), .x136(x136), .x137(x137), .x138(x138), .x139(x139),
        .x140(x140), .x141(x141), .x142(x142), .x143(x143), .x144(x144),
        .x145(x145), .x146(x146), .x147(x147), .x148(x148), .x149(x149),
        .x150(x150), .x151(x151), .x152(x152), .x153(x153), .x154(x154),
        .x155(x155), .x156(x156), .x157(x157), .x158(x158), .x159(x159),
        .x160(x160), .x161(x161), .x162(x162), .x163(x163), .x164(x164),
        .x165(x165), .x166(x166), .x167(x167), .x168(x168), .x169(x169),
        .x170(x170), .x171(x171), .x172(x172), .x173(x173), .x174(x174),
        .x175(x175), .x176(x176), .x177(x177), .x178(x178), .x179(x179),
        .x180(x180), .x181(x181), .x182(x182), .x183(x183), .x184(x184),
        .x185(x185), .x186(x186), .x187(x187), .x188(x188), .x189(x189),
        .x190(x190), .x191(x191), .x192(x192), .x193(x193), .x194(x194),
        .x195(x195), .x196(x196), .x197(x197), .x198(x198), .x199(x199),
        .x200(x200), .x201(x201), .x202(x202), .x203(x203), .x204(x204),
        .x205(x205), .x206(x206), .x207(x207), .x208(x208), .x209(x209),
        .x210(x210), .x211(x211), .x212(x212), .x213(x213), .x214(x214),
        .x215(x215), .x216(x216), .x217(x217), .x218(x218), .x219(x219),
        .x220(x220), .x221(x221), .x222(x222), .x223(x223), .x224(x224),
        .x225(x225), .x226(x226), .x227(x227), .x228(x228), .x229(x229),
        .x230(x230), .x231(x231), .x232(x232), .x233(x233), .x234(x234),
        .x235(x235), .x236(x236), .x237(x237), .x238(x238), .x239(x239),
        .x240(x240), .x241(x241), .x242(x242), .x243(x243), .x244(x244),
        .x245(x245), .x246(x246), .x247(x247), .x248(x248), .x249(x249),
        .x250(x250), .x251(x251), .x252(x252), .x253(x253), .x254(x254),
        .x255(x255), .x256(x256), .x257(x257), .x258(x258), .x259(x259),
        .x260(x260), .x261(x261), .x262(x262), .x263(x263), .x264(x264),
        .x265(x265), .x266(x266), .x267(x267), .x268(x268), .x269(x269),
        .x270(x270), .x271(x271), .x272(x272), .x273(x273), .x274(x274),
        .x275(x275), .x276(x276), .x277(x277), .x278(x278), .x279(x279),
        .x280(x280), .x281(x281), .x282(x282), .x283(x283), .x284(x284),
        .x285(x285), .x286(x286), .x287(x287), .x288(x288), .x289(x289),
        .x290(x290), .x291(x291), .x292(x292), .x293(x293), .x294(x294),
        .x295(x295), .x296(x296), .x297(x297), .x298(x298), .x299(x299),
        .x300(x300), .x301(x301), .x302(x302), .x303(x303), .x304(x304),
        .x305(x305), .x306(x306), .x307(x307), .x308(x308), .x309(x309),
        .x310(x310), .x311(x311),
        .y(y)
    );

    initial begin
        $display("Starting simulation...");

        // Open files
        buffer_in      = $fopen("input_data.txt", "r");
        buffer_weights = $fopen("weights_data.txt", "r");
        buffer_out     = $fopen("output_result.txt", "w");

        if (buffer_in == 0 || buffer_weights == 0) begin
            $display("Could not open input or weights file.");
            $finish;
        end

        // Read input data into array
        for (i = 0; i < 312; i = i + 1) begin
            r = $fscanf(buffer_in, "%h\n", input_data[i]);
            if (r == 0) begin
                $display("Error reading input_data.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(buffer_in);

        // Read weights data into array
        for (i = 0; i < 312; i = i + 1) begin
            r = $fscanf(buffer_weights, "%h\n", weights_data[i]);
            if (r == 0) begin
                $display("Error reading weights_data.txt at line %0d", i+1);
                $finish;
            end
        end
        $fclose(buffer_weights);

        $display("Files read successfully.");

        // Initialize regs to 0 first
        a0=0; a1=0; a2=0; a3=0; a4=0; a5=0; a6=0; a7=0; a8=0; a9=0;
        a10=0; a11=0; a12=0; a13=0; a14=0; a15=0; a16=0; a17=0; a18=0; a19=0;
        a20=0; a21=0; a22=0; a23=0; a24=0; a25=0; a26=0; a27=0; a28=0; a29=0;
        a30=0; a31=0; a32=0; a33=0; a34=0; a35=0; a36=0; a37=0; a38=0; a39=0;
        a40=0; a41=0; a42=0; a43=0; a44=0; a45=0; a46=0; a47=0; a48=0; a49=0;
        a50=0; a51=0; a52=0; a53=0; a54=0; a55=0; a56=0; a57=0; a58=0; a59=0;
        a60=0; a61=0; a62=0; a63=0; a64=0; a65=0; a66=0; a67=0; a68=0; a69=0;
        a70=0; a71=0; a72=0; a73=0; a74=0; a75=0; a76=0; a77=0; a78=0; a79=0;
        a80=0; a81=0; a82=0; a83=0; a84=0; a85=0; a86=0; a87=0; a88=0; a89=0;
        a90=0; a91=0; a92=0; a93=0; a94=0; a95=0; a96=0; a97=0; a98=0; a99=0;
        a100=0; a101=0; a102=0; a103=0; a104=0; a105=0; a106=0; a107=0; a108=0; a109=0;
        a110=0; a111=0; a112=0; a113=0; a114=0; a115=0; a116=0; a117=0; a118=0; a119=0;
        a120=0; a121=0; a122=0; a123=0; a124=0; a125=0; a126=0; a127=0; a128=0; a129=0;
        a130=0; a131=0; a132=0; a133=0; a134=0; a135=0; a136=0; a137=0; a138=0; a139=0;
        a140=0; a141=0; a142=0; a143=0; a144=0; a145=0; a146=0; a147=0; a148=0; a149=0;
        a150=0; a151=0; a152=0; a153=0; a154=0; a155=0; a156=0; a157=0; a158=0; a159=0;
        a160=0; a161=0; a162=0; a163=0; a164=0; a165=0; a166=0; a167=0; a168=0; a169=0;
        a170=0; a171=0; a172=0; a173=0; a174=0; a175=0; a176=0; a177=0; a178=0; a179=0;
        a180=0; a181=0; a182=0; a183=0; a184=0; a185=0; a186=0; a187=0; a188=0; a189=0;
        a190=0; a191=0; a192=0; a193=0; a194=0; a195=0; a196=0; a197=0; a198=0; a199=0;
        a200=0; a201=0; a202=0; a203=0; a204=0; a205=0; a206=0; a207=0; a208=0; a209=0;
        a210=0; a211=0; a212=0; a213=0; a214=0; a215=0; a216=0; a217=0; a218=0; a219=0;
        a220=0; a221=0; a222=0; a223=0; a224=0; a225=0; a226=0; a227=0; a228=0; a229=0;
        a230=0; a231=0; a232=0; a233=0; a234=0; a235=0; a236=0; a237=0; a238=0; a239=0;
        a240=0; a241=0; a242=0; a243=0; a244=0; a245=0; a246=0; a247=0; a248=0; a249=0;
        a250=0; a251=0; a252=0; a253=0; a254=0; a255=0; a256=0; a257=0; a258=0; a259=0;
        a260=0; a261=0; a262=0; a263=0; a264=0; a265=0; a266=0; a267=0; a268=0; a269=0;
        a270=0; a271=0; a272=0; a273=0; a274=0; a275=0; a276=0; a277=0; a278=0; a279=0;
        a280=0; a281=0; a282=0; a283=0; a284=0; a285=0; a286=0; a287=0; a288=0; a289=0;
        a290=0; a291=0; a292=0; a293=0; a294=0; a295=0; a296=0; a297=0; a298=0; a299=0;
        a300=0; a301=0; a302=0; a303=0; a304=0; a305=0; a306=0; a307=0; a308=0; a309=0;
        a310=0; a311=0;
        x0=0; x1=0; x2=0; x3=0; x4=0; x5=0; x6=0; x7=0; x8=0; x9=0;
        x10=0; x11=0; x12=0; x13=0; x14=0; x15=0; x16=0; x17=0; x18=0; x19=0;
        x20=0; x21=0; x22=0; x23=0; x24=0; x25=0; x26=0; x27=0; x28=0; x29=0;
        x30=0; x31=0; x32=0; x33=0; x34=0; x35=0; x36=0; x37=0; x38=0; x39=0;
        x40=0; x41=0; x42=0; x43=0; x44=0; x45=0; x46=0; x47=0; x48=0; x49=0;
        x50=0; x51=0; x52=0; x53=0; x54=0; x55=0; x56=0; x57=0; x58=0; x59=0;
        x60=0; x61=0; x62=0; x63=0; x64=0; x65=0; x66=0; x67=0; x68=0; x69=0;
        x70=0; x71=0; x72=0; x73=0; x74=0; x75=0; x76=0; x77=0; x78=0; x79=0;
        x80=0; x81=0; x82=0; x83=0; x84=0; x85=0; x86=0; x87=0; x88=0; x89=0;
        x90=0; x91=0; x92=0; x93=0; x94=0; x95=0; x96=0; x97=0; x98=0; x99=0;
        x100=0; x101=0; x102=0; x103=0; x104=0; x105=0; x106=0; x107=0; x108=0; x109=0;
        x110=0; x111=0; x112=0; x113=0; x114=0; x115=0; x116=0; x117=0; x118=0; x119=0;
        x120=0; x121=0; x122=0; x123=0; x124=0; x125=0; x126=0; x127=0; x128=0; x129=0;
        x130=0; x131=0; x132=0; x133=0; x134=0; x135=0; x136=0; x137=0; x138=0; x139=0;
        x140=0; x141=0; x142=0; x143=0; x144=0; x145=0; x146=0; x147=0; x148=0; x149=0;
        x150=0; x151=0; x152=0; x153=0; x154=0; x155=0; x156=0; x157=0; x158=0; x159=0;
        x160=0; x161=0; x162=0; x163=0; x164=0; x165=0; x166=0; x167=0; x168=0; x169=0;
        x170=0; x171=0; x172=0; x173=0; x174=0; x175=0; x176=0; x177=0; x178=0; x179=0;
        x180=0; x181=0; x182=0; x183=0; x184=0; x185=0; x186=0; x187=0; x188=0; x189=0;
        x190=0; x191=0; x192=0; x193=0; x194=0; x195=0; x196=0; x197=0; x198=0; x199=0;
        x200=0; x201=0; x202=0; x203=0; x204=0; x205=0; x206=0; x207=0; x208=0; x209=0;
        x210=0; x211=0; x212=0; x213=0; x214=0; x215=0; x216=0; x217=0; x218=0; x219=0;
        x220=0; x221=0; x222=0; x223=0; x224=0; x225=0; x226=0; x227=0; x228=0; x229=0;
        x230=0; x231=0; x232=0; x233=0; x234=0; x235=0; x236=0; x237=0; x238=0; x239=0;
        x240=0; x241=0; x242=0; x243=0; x244=0; x245=0; x246=0; x247=0; x248=0; x249=0;
        x250=0; x251=0; x252=0; x253=0; x254=0; x255=0; x256=0; x257=0; x258=0; x259=0;
        x260=0; x261=0; x262=0; x263=0; x264=0; x265=0; x266=0; x267=0; x268=0; x269=0;
        x270=0; x271=0; x272=0; x273=0; x274=0; x275=0; x276=0; x277=0; x278=0; x279=0;
        x280=0; x281=0; x282=0; x283=0; x284=0; x285=0; x286=0; x287=0; x288=0; x289=0;
        x290=0; x291=0; x292=0; x293=0; x294=0; x295=0; x296=0; x297=0; x298=0; x299=0;
        x300=0; x301=0; x302=0; x303=0; x304=0; x305=0; x306=0; x307=0; x308=0; x309=0;
        x310=0; x311=0;

        // Wait a few cycles
        repeat(5) @(posedge clk);

        // Assign weights_data to a0..a9, input_data to x0..x9
        a0 = weights_data[0]; a1 = weights_data[1]; a2 = weights_data[2];
        a3 = weights_data[3]; a4 = weights_data[4]; a5 = weights_data[5];
        a6 = weights_data[6]; a7 = weights_data[7]; a8 = weights_data[8];
        a9 = weights_data[9]; a10 = weights_data[10]; a11 = weights_data[11];
        a12 = weights_data[12]; a13 = weights_data[13]; a14 = weights_data[14];
        a15 = weights_data[15]; a16 = weights_data[16]; a17 = weights_data[17];
        a18 = weights_data[18]; a19 = weights_data[19]; a20 = weights_data[20];
        a21 = weights_data[21]; a22 = weights_data[22]; a23 = weights_data[23];
        a24 = weights_data[24]; a25 = weights_data[25]; a26 = weights_data[26];
        a27 = weights_data[27]; a28 = weights_data[28]; a29 = weights_data[29];
        a30 = weights_data[30]; a31 = weights_data[31]; a32 = weights_data[32];
        a33 = weights_data[33]; a34 = weights_data[34]; a35 = weights_data[35];
        a36 = weights_data[36]; a37 = weights_data[37]; a38 = weights_data[38];
        a39 = weights_data[39]; a40 = weights_data[40]; a41 = weights_data[41];
        a42 = weights_data[42]; a43 = weights_data[43]; a44 = weights_data[44];
        a45 = weights_data[45]; a46 = weights_data[46]; a47 = weights_data[47];
        a48 = weights_data[48]; a49 = weights_data[49]; a50 = weights_data[50];
        a51 = weights_data[51]; a52 = weights_data[52]; a53 = weights_data[53];
        a54 = weights_data[54]; a55 = weights_data[55]; a56 = weights_data[56];
        a57 = weights_data[57]; a58 = weights_data[58]; a59 = weights_data[59];
        a60 = weights_data[60]; a61 = weights_data[61]; a62 = weights_data[62];
        a63 = weights_data[63]; a64 = weights_data[64]; a65 = weights_data[65];
        a66 = weights_data[66]; a67 = weights_data[67]; a68 = weights_data[68];
        a69 = weights_data[69]; a70 = weights_data[70]; a71 = weights_data[71];
        a72 = weights_data[72]; a73 = weights_data[73]; a74 = weights_data[74];
        a75 = weights_data[75]; a76 = weights_data[76]; a77 = weights_data[77];
        a78 = weights_data[78]; a79 = weights_data[79]; a80 = weights_data[80];
        a81 = weights_data[81]; a82 = weights_data[82]; a83 = weights_data[83];
        a84 = weights_data[84]; a85 = weights_data[85]; a86 = weights_data[86];
        a87 = weights_data[87]; a88 = weights_data[88]; a89 = weights_data[89];
        a90 = weights_data[90]; a91 = weights_data[91]; a92 = weights_data[92];
        a93 = weights_data[93]; a94 = weights_data[94]; a95 = weights_data[95];
        a96 = weights_data[96]; a97 = weights_data[97]; a98 = weights_data[98];
        a99 = weights_data[99]; a100 = weights_data[100]; a101 = weights_data[101];
        a102 = weights_data[102]; a103 = weights_data[103]; a104 = weights_data[104];
        a105 = weights_data[105]; a106 = weights_data[106]; a107 = weights_data[107];
        a108 = weights_data[108]; a109 = weights_data[109]; a110 = weights_data[110];
        a111 = weights_data[111]; a112 = weights_data[112]; a113 = weights_data[113];
        a114 = weights_data[114]; a115 = weights_data[115]; a116 = weights_data[116];
        a117 = weights_data[117]; a118 = weights_data[118]; a119 = weights_data[119];
        a120 = weights_data[120]; a121 = weights_data[121]; a122 = weights_data[122];
        a123 = weights_data[123]; a124 = weights_data[124]; a125 = weights_data[125];
        a126 = weights_data[126]; a127 = weights_data[127]; a128 = weights_data[128];
        a129 = weights_data[129]; a130 = weights_data[130]; a131 = weights_data[131];
        a132 = weights_data[132]; a133 = weights_data[133]; a134 = weights_data[134];
        a135 = weights_data[135]; a136 = weights_data[136]; a137 = weights_data[137];
        a138 = weights_data[138]; a139 = weights_data[139]; a140 = weights_data[140];
        a141 = weights_data[141]; a142 = weights_data[142]; a143 = weights_data[143];
        a144 = weights_data[144]; a145 = weights_data[145]; a146 = weights_data[146];
        a147 = weights_data[147]; a148 = weights_data[148]; a149 = weights_data[149];
        a150 = weights_data[150]; a151 = weights_data[151]; a152 = weights_data[152];
        a153 = weights_data[153]; a154 = weights_data[154]; a155 = weights_data[155];
        a156 = weights_data[156]; a157 = weights_data[157]; a158 = weights_data[158];
        a159 = weights_data[159]; a160 = weights_data[160]; a161 = weights_data[161];
        a162 = weights_data[162]; a163 = weights_data[163]; a164 = weights_data[164];
        a165 = weights_data[165]; a166 = weights_data[166]; a167 = weights_data[167];
        a168 = weights_data[168]; a169 = weights_data[169]; a170 = weights_data[170];
        a171 = weights_data[171]; a172 = weights_data[172]; a173 = weights_data[173];
        a174 = weights_data[174]; a175 = weights_data[175]; a176 = weights_data[176];
        a177 = weights_data[177]; a178 = weights_data[178]; a179 = weights_data[179];
        a180 = weights_data[180]; a181 = weights_data[181]; a182 = weights_data[182];
        a183 = weights_data[183]; a184 = weights_data[184]; a185 = weights_data[185];
        a186 = weights_data[186]; a187 = weights_data[187]; a188 = weights_data[188];
        a189 = weights_data[189]; a190 = weights_data[190]; a191 = weights_data[191];
        a192 = weights_data[192]; a193 = weights_data[193]; a194 = weights_data[194];
        a195 = weights_data[195]; a196 = weights_data[196]; a197 = weights_data[197];
        a198 = weights_data[198]; a199 = weights_data[199]; a200 = weights_data[200];
        a201 = weights_data[201]; a202 = weights_data[202]; a203 = weights_data[203];
        a204 = weights_data[204]; a205 = weights_data[205]; a206 = weights_data[206];
        a207 = weights_data[207]; a208 = weights_data[208]; a209 = weights_data[209];
        a210 = weights_data[210]; a211 = weights_data[211]; a212 = weights_data[212];
        a213 = weights_data[213]; a214 = weights_data[214]; a215 = weights_data[215];
        a216 = weights_data[216]; a217 = weights_data[217]; a218 = weights_data[218];
        a219 = weights_data[219]; a220 = weights_data[220]; a221 = weights_data[221];
        a222 = weights_data[222]; a223 = weights_data[223]; a224 = weights_data[224];
        a225 = weights_data[225]; a226 = weights_data[226]; a227 = weights_data[227];
        a228 = weights_data[228]; a229 = weights_data[229]; a230 = weights_data[230];
        a231 = weights_data[231]; a232 = weights_data[232]; a233 = weights_data[233];
        a234 = weights_data[234]; a235 = weights_data[235]; a236 = weights_data[236];
        a237 = weights_data[237]; a238 = weights_data[238]; a239 = weights_data[239];
        a240 = weights_data[240]; a241 = weights_data[241]; a242 = weights_data[242];
        a243 = weights_data[243]; a244 = weights_data[244]; a245 = weights_data[245];
        a246 = weights_data[246]; a247 = weights_data[247]; a248 = weights_data[248];
        a249 = weights_data[249]; a250 = weights_data[250]; a251 = weights_data[251];
        a252 = weights_data[252]; a253 = weights_data[253]; a254 = weights_data[254];
        a255 = weights_data[255]; a256 = weights_data[256]; a257 = weights_data[257];
        a258 = weights_data[258]; a259 = weights_data[259]; a260 = weights_data[260];
        a261 = weights_data[261]; a262 = weights_data[262]; a263 = weights_data[263];
        a264 = weights_data[264]; a265 = weights_data[265]; a266 = weights_data[266];
        a267 = weights_data[267]; a268 = weights_data[268]; a269 = weights_data[269];
        a270 = weights_data[270]; a271 = weights_data[271]; a272 = weights_data[272];
        a273 = weights_data[273]; a274 = weights_data[274]; a275 = weights_data[275];
        a276 = weights_data[276]; a277 = weights_data[277]; a278 = weights_data[278];
        a279 = weights_data[279]; a280 = weights_data[280]; a281 = weights_data[281];
        a282 = weights_data[282]; a283 = weights_data[283]; a284 = weights_data[284];
        a285 = weights_data[285]; a286 = weights_data[286]; a287 = weights_data[287];
        a288 = weights_data[288]; a289 = weights_data[289]; a290 = weights_data[290];
        a291 = weights_data[291]; a292 = weights_data[292]; a293 = weights_data[293];
        a294 = weights_data[294]; a295 = weights_data[295]; a296 = weights_data[296];
        a297 = weights_data[297]; a298 = weights_data[298]; a299 = weights_data[299];
        a300 = weights_data[300]; a301 = weights_data[301]; a302 = weights_data[302];
        a303 = weights_data[303]; a304 = weights_data[304]; a305 = weights_data[305];
        a306 = weights_data[306]; a307 = weights_data[307]; a308 = weights_data[308];
        a309 = weights_data[309]; a310 = weights_data[310]; a311 = weights_data[311];

        x0 = input_data[0];  x1 = input_data[1];  x2 = input_data[2];
        x3 = input_data[3];  x4 = input_data[4];  x5 = input_data[5];
        x6 = input_data[6];  x7 = input_data[7];  x8 = input_data[8];
        x9 = input_data[9];  x10 = input_data[10];  x11 = input_data[11];
        x12 = input_data[12];  x13 = input_data[13];  x14 = input_data[14];
        x15 = input_data[15];  x16 = input_data[16];  x17 = input_data[17];
        x18 = input_data[18];  x19 = input_data[19];  x20 = input_data[20];
        x21 = input_data[21];  x22 = input_data[22];  x23 = input_data[23];
        x24 = input_data[24];  x25 = input_data[25];  x26 = input_data[26];
        x27 = input_data[27];  x28 = input_data[28];  x29 = input_data[29];
        x30 = input_data[30];  x31 = input_data[31];  x32 = input_data[32];
        x33 = input_data[33];  x34 = input_data[34];  x35 = input_data[35];
        x36 = input_data[36];  x37 = input_data[37];  x38 = input_data[38];
        x39 = input_data[39];  x40 = input_data[40];  x41 = input_data[41];
        x42 = input_data[42];  x43 = input_data[43];  x44 = input_data[44];
        x45 = input_data[45];  x46 = input_data[46];  x47 = input_data[47];
        x48 = input_data[48];  x49 = input_data[49];  x50 = input_data[50];
        x51 = input_data[51];  x52 = input_data[52];  x53 = input_data[53];
        x54 = input_data[54];  x55 = input_data[55];  x56 = input_data[56];
        x57 = input_data[57];  x58 = input_data[58];  x59 = input_data[59];
        x60 = input_data[60];  x61 = input_data[61];  x62 = input_data[62];
        x63 = input_data[63];  x64 = input_data[64];  x65 = input_data[65];
        x66 = input_data[66];  x67 = input_data[67];  x68 = input_data[68];
        x69 = input_data[69];  x70 = input_data[70];  x71 = input_data[71];
        x72 = input_data[72];  x73 = input_data[73];  x74 = input_data[74];
        x75 = input_data[75];  x76 = input_data[76];  x77 = input_data[77];
        x78 = input_data[78];  x79 = input_data[79];  x80 = input_data[80];
        x81 = input_data[81];  x82 = input_data[82];  x83 = input_data[83];
        x84 = input_data[84];  x85 = input_data[85];  x86 = input_data[86];
        x87 = input_data[87];  x88 = input_data[88];  x89 = input_data[89];
        x90 = input_data[90];  x91 = input_data[91];  x92 = input_data[92];
        x93 = input_data[93];  x94 = input_data[94];  x95 = input_data[95];
        x96 = input_data[96];  x97 = input_data[97];  x98 = input_data[98];
        x99 = input_data[99];  x100 = input_data[100];  x101 = input_data[101];
        x102 = input_data[102];  x103 = input_data[103];  x104 = input_data[104];
        x105 = input_data[105];  x106 = input_data[106];  x107 = input_data[107];
        x108 = input_data[108];  x109 = input_data[109];  x110 = input_data[110];
        x111 = input_data[111];  x112 = input_data[112];  x113 = input_data[113];
        x114 = input_data[114];  x115 = input_data[115];  x116 = input_data[116];
        x117 = input_data[117];  x118 = input_data[118];  x119 = input_data[119];
        x120 = input_data[120];  x121 = input_data[121];  x122 = input_data[122];
        x123 = input_data[123];  x124 = input_data[124];  x125 = input_data[125];
        x126 = input_data[126];  x127 = input_data[127];  x128 = input_data[128];
        x129 = input_data[129];  x130 = input_data[130];  x131 = input_data[131];
        x132 = input_data[132];  x133 = input_data[133];  x134 = input_data[134];
        x135 = input_data[135];  x136 = input_data[136];  x137 = input_data[137];
        x138 = input_data[138];  x139 = input_data[139];  x140 = input_data[140];
        x141 = input_data[141];  x142 = input_data[142];  x143 = input_data[143];
        x144 = input_data[144];  x145 = input_data[145];  x146 = input_data[146];
        x147 = input_data[147];  x148 = input_data[148];  x149 = input_data[149];
        x150 = input_data[150];  x151 = input_data[151];  x152 = input_data[152];
        x153 = input_data[153];  x154 = input_data[154];  x155 = input_data[155];
        x156 = input_data[156];  x157 = input_data[157];  x158 = input_data[158];
        x159 = input_data[159];  x160 = input_data[160];  x161 = input_data[161];
        x162 = input_data[162];  x163 = input_data[163];  x164 = input_data[164];
        x165 = input_data[165];  x166 = input_data[166];  x167 = input_data[167];
        x168 = input_data[168];  x169 = input_data[169];  x170 = input_data[170];
        x171 = input_data[171];  x172 = input_data[172];  x173 = input_data[173];
        x174 = input_data[174];  x175 = input_data[175];  x176 = input_data[176];
        x177 = input_data[177];  x178 = input_data[178];  x179 = input_data[179];
        x180 = input_data[180];  x181 = input_data[181];  x182 = input_data[182];
        x183 = input_data[183];  x184 = input_data[184];  x185 = input_data[185];
        x186 = input_data[186];  x187 = input_data[187];  x188 = input_data[188];
        x189 = input_data[189];  x190 = input_data[190];  x191 = input_data[191];
        x192 = input_data[192];  x193 = input_data[193];  x194 = input_data[194];
        x195 = input_data[195];  x196 = input_data[196];  x197 = input_data[197];
        x198 = input_data[198];  x199 = input_data[199];  x200 = input_data[200];
        x201 = input_data[201];  x202 = input_data[202];  x203 = input_data[203];
        x204 = input_data[204];  x205 = input_data[205];  x206 = input_data[206];
        x207 = input_data[207];  x208 = input_data[208];  x209 = input_data[209];
        x210 = input_data[210];  x211 = input_data[211];  x212 = input_data[212];
        x213 = input_data[213];  x214 = input_data[214];  x215 = input_data[215];
        x216 = input_data[216];  x217 = input_data[217];  x218 = input_data[218];
        x219 = input_data[219];  x220 = input_data[220];  x221 = input_data[221];
        x222 = input_data[222];  x223 = input_data[223];  x224 = input_data[224];
        x225 = input_data[225];  x226 = input_data[226];  x227 = input_data[227];
        x228 = input_data[228];  x229 = input_data[229];  x230 = input_data[230];
        x231 = input_data[231];  x232 = input_data[232];  x233 = input_data[233];
        x234 = input_data[234];  x235 = input_data[235];  x236 = input_data[236];
        x237 = input_data[237];  x238 = input_data[238];  x239 = input_data[239];
        x240 = input_data[240];  x241 = input_data[241];  x242 = input_data[242];
        x243 = input_data[243];  x244 = input_data[244];  x245 = input_data[245];
        x246 = input_data[246];  x247 = input_data[247];  x248 = input_data[248];
        x249 = input_data[249];  x250 = input_data[250];  x251 = input_data[251];
        x252 = input_data[252];  x253 = input_data[253];  x254 = input_data[254];
        x255 = input_data[255];  x256 = input_data[256];  x257 = input_data[257];
        x258 = input_data[258];  x259 = input_data[259];  x260 = input_data[260];
        x261 = input_data[261];  x262 = input_data[262];  x263 = input_data[263];
        x264 = input_data[264];  x265 = input_data[265];  x266 = input_data[266];
        x267 = input_data[267];  x268 = input_data[268];  x269 = input_data[269];
        x270 = input_data[270];  x271 = input_data[271];  x272 = input_data[272];
        x273 = input_data[273];  x274 = input_data[274];  x275 = input_data[275];
        x276 = input_data[276];  x277 = input_data[277];  x278 = input_data[278];
        x279 = input_data[279];  x280 = input_data[280];  x281 = input_data[281];
        x282 = input_data[282];  x283 = input_data[283];  x284 = input_data[284];
        x285 = input_data[285];  x286 = input_data[286];  x287 = input_data[287];
        x288 = input_data[288];  x289 = input_data[289];  x290 = input_data[290];
        x291 = input_data[291];  x292 = input_data[292];  x293 = input_data[293];
        x294 = input_data[294];  x295 = input_data[295];  x296 = input_data[296];
        x297 = input_data[297];  x298 = input_data[298];  x299 = input_data[299];
        x300 = input_data[300];  x301 = input_data[301];  x302 = input_data[302];
        x303 = input_data[303];  x304 = input_data[304];  x305 = input_data[305];
        x306 = input_data[306];  x307 = input_data[307];  x308 = input_data[308];
        x309 = input_data[309];  x310 = input_data[310];  x311 = input_data[311];

        $display("Starting SVM computation...");
        // Wait a few clock cycles so the multiplication/summation can settle
        repeat(5) @(posedge clk);

        $display("Computation finished. y = %d", y);
        $fdisplay(buffer_out, "%d", y);
        $fclose(buffer_out);

        $display("Simulation complete.");
        $finish;
    end

endmodule
