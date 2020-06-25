/* Verilog module written by vlog2Verilog (qflow) */

module map9v3(
    input [8:0] N,
    input clock,
    output [7:0] counter,
    output done,
    output [8:0] dp,
    input reset,
    output [7:0] sr,
    input start
);

wire vdd = 1'b1;
wire gnd = 1'b0;

wire [8:0] N ;
wire _60_ ;
wire _19_ ;
wire _57_ ;
wire _95_ ;
wire _16_ ;
wire _54_ ;
wire _92_ ;
wire _89_ ;
wire _13_ ;
wire _51_ ;
wire clock ;
wire _7_ ;
wire _48_ ;
wire _86_ ;
wire _10_ ;
wire _4_ ;
wire _45_ ;
wire _83_ ;
wire _1_ ;
wire _42_ ;
wire _80_ ;
wire _39_ ;
wire _112_ ;
wire _77_ ;
wire _109_ ;
wire _36_ ;
wire _74_ ;
wire _106_ ;
wire _33_ ;
wire _71_ ;
wire _103_ ;
wire _68_ ;
wire _30_ ;
wire _27_ ;
wire _100_ ;
wire _65_ ;
wire start ;
wire _24_ ;
wire _62_ ;
wire _59_ ;
wire _97_ ;
wire _21_ ;
wire _18_ ;
wire _56_ ;
wire _94_ ;
wire _15_ ;
wire _53_ ;
wire _91_ ;
wire _9_ ;
wire _88_ ;
wire _12_ ;
wire _50_ ;
wire _6_ ;
wire _47_ ;
wire _85_ ;
wire [7:0] sr ;
wire [7:0] counter ;
wire [7:0] _3_ ;
wire _44_ ;
wire _82_ ;
wire done ;
wire [7:0] _114_ ;
wire _79_ ;
wire [7:0] _0_ ;
wire _41_ ;
wire _38_ ;
wire [7:0] _111_ ;
wire _76_ ;
wire _108_ ;
wire _35_ ;
wire _73_ ;
wire _105_ ;
wire _32_ ;
wire _70_ ;
wire _29_ ;
wire _102_ ;
wire _67_ ;
wire [4:0] state ;
wire [8:0] dp ;
wire [1:0] startbuf ;
wire _26_ ;
wire _64_ ;
wire _102__bF$buf0 ;
wire _102__bF$buf1 ;
wire _102__bF$buf2 ;
wire _102__bF$buf3 ;
wire _99_ ;
wire _23_ ;
wire _61_ ;
wire _8__bF$buf0 ;
wire _8__bF$buf1 ;
wire _8__bF$buf2 ;
wire _8__bF$buf3 ;
wire _8__bF$buf4 ;
wire _58_ ;
wire _96_ ;
wire _20_ ;
wire _17_ ;
wire _55_ ;
wire _93_ ;
wire _14_ ;
wire _52_ ;
wire _90_ ;
wire _8_ ;
wire _49_ ;
wire _87_ ;
wire _11_ ;
wire _5_ ;
wire _46_ ;
wire _84_ ;
wire clock_bF$buf0 ;
wire clock_bF$buf1 ;
wire clock_bF$buf2 ;
wire clock_bF$buf3 ;
wire clock_bF$buf4 ;
wire [8:0] _2_ ;
wire _43_ ;
wire _81_ ;
wire [8:0] _113_ ;
wire _78_ ;
wire _40_ ;
wire _37_ ;
wire _110_ ;
wire _75_ ;
wire _107_ ;
wire _34_ ;
wire _72_ ;
wire _104_ ;
wire _69_ ;
wire _31_ ;
wire _28_ ;
wire _101_ ;
wire _66_ ;
wire _25_ ;
wire _63_ ;
wire reset ;
wire _98_ ;
wire _22_ ;

OAI21X1 _168_ (
    .A(_114_[4]),
    .B(_102__bF$buf0),
    .C(_91_),
    .Y(_27_)
);

FILL SFILL20080x16100 (
);

FILL SFILL6320x14100 (
);

NOR2X1 _130_ (
    .A(_114_[0]),
    .B(_103_),
    .Y(_104_)
);

FILL SFILL6800x16100 (
);

FILL SFILL18800x6100 (
);

INVX1 _224_ (
    .A(N[7]),
    .Y(_72_)
);

BUFX2 _262_ (
    .A(_113_[5]),
    .Y(dp[5])
);

INVX1 _127_ (
    .A(_113_[1]),
    .Y(_101_)
);

AOI21X1 _165_ (
    .A(_102__bF$buf2),
    .B(_110_),
    .C(_25_),
    .Y(_3_[3])
);

FILL SFILL18480x14100 (
);

FILL SFILL6640x12100 (
);

BUFX2 _259_ (
    .A(_113_[2]),
    .Y(dp[2])
);

DFFSR _297_ (
    .Q(_113_[0]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_2_[0])
);

INVX1 _221_ (
    .A(_111_[5]),
    .Y(_70_)
);

INVX1 _124_ (
    .A(startbuf[0]),
    .Y(_99_)
);

OAI21X1 _162_ (
    .A(_114_[1]),
    .B(_102__bF$buf1),
    .C(_91_),
    .Y(_24_)
);

OAI21X1 _218_ (
    .A(N[5]),
    .B(_52_),
    .C(N[6]),
    .Y(_67_)
);

BUFX2 _256_ (
    .A(_112_),
    .Y(done)
);

DFFSR _294_ (
    .Q(_114_[5]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_3_[5])
);

FILL SFILL7440x10100 (
);

AOI21X1 _159_ (
    .A(_19_),
    .B(_20_),
    .C(_21_),
    .Y(_22_)
);

XOR2X1 _197_ (
    .A(_43_),
    .B(_111_[2]),
    .Y(_49_)
);

NAND2X1 _121_ (
    .A(_91_),
    .B(_96_),
    .Y(_7_)
);

FILL SFILL6800x14100 (
);

OAI21X1 _215_ (
    .A(_58_),
    .B(_59_),
    .C(_64_),
    .Y(_0_[4])
);

BUFX2 _253_ (
    .A(_111_[5]),
    .Y(counter[5])
);

NOR3X1 _118_ (
    .A(_111_[5]),
    .B(_111_[4]),
    .C(_111_[6]),
    .Y(_94_)
);

DFFSR _291_ (
    .Q(_114_[2]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(_3_[2])
);

XNOR2X1 _156_ (
    .A(_114_[5]),
    .B(_114_[7]),
    .Y(_19_)
);

NAND2X1 _194_ (
    .A(_41_),
    .B(_46_),
    .Y(_0_[1])
);

FILL FILL24080x100 (
);

DFFSR _288_ (
    .Q(_111_[7]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_0_[7])
);

NOR2X1 _212_ (
    .A(_60_),
    .B(_61_),
    .Y(_62_)
);

BUFX2 _250_ (
    .A(_111_[2]),
    .Y(counter[2])
);

DFFSR _306_ (
    .Q(_112_),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(_1_)
);

INVX4 _115_ (
    .A(state[0]),
    .Y(_91_)
);

INVX1 _153_ (
    .A(_113_[0]),
    .Y(_17_)
);

OAI21X1 _209_ (
    .A(N[5]),
    .B(_52_),
    .C(state[0]),
    .Y(_59_)
);

INVX1 _191_ (
    .A(_43_),
    .Y(_44_)
);

FILL SFILL19760x4100 (
);

INVX8 _247_ (
    .A(reset),
    .Y(_8_)
);

FILL SFILL7600x100 (
);

DFFSR _285_ (
    .Q(_111_[4]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_0_[4])
);

OAI21X1 _188_ (
    .A(_38_),
    .B(_40_),
    .C(state[0]),
    .Y(_41_)
);

FILL SFILL20080x12100 (
);

DFFSR _303_ (
    .Q(_113_[6]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_2_[6])
);

INVX1 _150_ (
    .A(_113_[8]),
    .Y(_15_)
);

FILL SFILL18640x14100 (
);

FILL SFILL6800x12100 (
);

OAI21X1 _206_ (
    .A(state[0]),
    .B(_56_),
    .C(_53_),
    .Y(_0_[3])
);

FILL SFILL6960x8100 (
);

AND2X2 _244_ (
    .A(_90_),
    .B(_86_),
    .Y(_0_[7])
);

DFFSR _282_ (
    .Q(_111_[1]),
    .CLK(clock_bF$buf1),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(_0_[1])
);

INVX1 _147_ (
    .A(_113_[7]),
    .Y(_13_)
);

NOR2X1 _185_ (
    .A(N[1]),
    .B(N[2]),
    .Y(_38_)
);

FILL SFILL20560x2100 (
);

DFFSR _279_ (
    .Q(startbuf[0]),
    .CLK(clock_bF$buf1),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(start)
);

DFFSR _300_ (
    .Q(_113_[3]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_2_[3])
);

OAI21X1 _203_ (
    .A(_111_[2]),
    .B(_43_),
    .C(_111_[3]),
    .Y(_54_)
);

NAND3X1 _241_ (
    .A(state[3]),
    .B(_87_),
    .C(_80_),
    .Y(_88_)
);

FILL SFILL7280x4100 (
);

INVX1 _144_ (
    .A(_113_[6]),
    .Y(_11_)
);

NOR2X1 _182_ (
    .A(_111_[0]),
    .B(_102__bF$buf3),
    .Y(_36_)
);

NAND3X1 _238_ (
    .A(_72_),
    .B(N[8]),
    .C(_73_),
    .Y(_85_)
);

DFFSR _276_ (
    .Q(state[2]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_5_)
);

AOI21X1 _179_ (
    .A(_33_),
    .B(_31_),
    .C(state[0]),
    .Y(_1_)
);

NOR2X1 _200_ (
    .A(N[3]),
    .B(N[4]),
    .Y(_51_)
);

INVX1 _141_ (
    .A(_113_[5]),
    .Y(_9_)
);

FILL FILL23920x16100 (
);

OAI21X1 _235_ (
    .A(state[0]),
    .B(_82_),
    .C(_76_),
    .Y(_0_[6])
);

FILL SFILL7920x100 (
);

FILL FILL23920x100 (
);

BUFX2 _273_ (
    .A(_114_[7]),
    .Y(sr[7])
);

FILL SFILL20240x2100 (
);

INVX1 _138_ (
    .A(_113_[4]),
    .Y(_109_)
);

INVX1 _176_ (
    .A(_112_),
    .Y(_31_)
);

BUFX2 BUFX2_insert5 (
    .A(_102_),
    .Y(_102__bF$buf3)
);

BUFX2 BUFX2_insert6 (
    .A(_102_),
    .Y(_102__bF$buf2)
);

BUFX2 BUFX2_insert7 (
    .A(_102_),
    .Y(_102__bF$buf1)
);

BUFX2 BUFX2_insert8 (
    .A(_102_),
    .Y(_102__bF$buf0)
);

BUFX2 BUFX2_insert9 (
    .A(_8_),
    .Y(_8__bF$buf4)
);

FILL SFILL18960x10100 (
);

NOR2X1 _232_ (
    .A(_79_),
    .B(_77_),
    .Y(_80_)
);

BUFX2 _270_ (
    .A(_114_[4]),
    .Y(sr[4])
);

INVX1 _135_ (
    .A(_113_[3]),
    .Y(_107_)
);

FILL SFILL7280x2100 (
);

AOI21X1 _173_ (
    .A(_102__bF$buf1),
    .B(_16_),
    .C(_29_),
    .Y(_3_[7])
);

NAND2X1 _229_ (
    .A(_92_),
    .B(_93_),
    .Y(_77_)
);

FILL FILL24080x16100 (
);

BUFX2 _267_ (
    .A(_114_[1]),
    .Y(sr[1])
);

FILL SFILL20240x12100 (
);

INVX1 _132_ (
    .A(_113_[2]),
    .Y(_105_)
);

OAI21X1 _170_ (
    .A(_114_[5]),
    .B(_102__bF$buf0),
    .C(_91_),
    .Y(_28_)
);

FILL SFILL18640x10100 (
);

OAI21X1 _226_ (
    .A(N[7]),
    .B(_66_),
    .C(state[0]),
    .Y(_74_)
);

FILL SFILL18640x8100 (
);

FILL SFILL6960x4100 (
);

BUFX2 _264_ (
    .A(_113_[7]),
    .Y(dp[7])
);

FILL SFILL7760x100 (
);

NAND3X1 _129_ (
    .A(state[2]),
    .B(_91_),
    .C(_102__bF$buf3),
    .Y(_103_)
);

AOI21X1 _167_ (
    .A(_102__bF$buf2),
    .B(_10_),
    .C(_26_),
    .Y(_3_[4])
);

FILL SFILL7600x6100 (
);

DFFSR _299_ (
    .Q(_113_[2]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(_2_[2])
);

AOI22X1 _223_ (
    .A(state[0]),
    .B(_68_),
    .C(_69_),
    .D(_71_),
    .Y(_0_[5])
);

BUFX2 _261_ (
    .A(_113_[4]),
    .Y(dp[4])
);

OAI21X1 _126_ (
    .A(_97_),
    .B(_100_),
    .C(_98_),
    .Y(_6_)
);

OAI21X1 _164_ (
    .A(_114_[2]),
    .B(_102__bF$buf2),
    .C(_91_),
    .Y(_25_)
);

FILL FILL24080x14100 (
);

BUFX2 _258_ (
    .A(_113_[1]),
    .Y(dp[1])
);

DFFSR _296_ (
    .Q(_114_[7]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_3_[7])
);

OAI21X1 _199_ (
    .A(N[3]),
    .B(_40_),
    .C(N[4]),
    .Y(_50_)
);

OAI21X1 _220_ (
    .A(_111_[4]),
    .B(_55_),
    .C(_111_[5]),
    .Y(_69_)
);

INVX1 _123_ (
    .A(state[4]),
    .Y(_98_)
);

NOR2X1 _161_ (
    .A(_23_),
    .B(_22_),
    .Y(_3_[0])
);

NAND3X1 _217_ (
    .A(_39_),
    .B(_51_),
    .C(_65_),
    .Y(_66_)
);

FILL FILL23920x12100 (
);

FILL SFILL18640x6100 (
);

BUFX2 _255_ (
    .A(_111_[7]),
    .Y(counter[7])
);

FILL SFILL6960x2100 (
);

DFFSR _293_ (
    .Q(_114_[4]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_3_[4])
);

FILL SFILL8080x100 (
);

OAI21X1 _158_ (
    .A(_19_),
    .B(_20_),
    .C(state[3]),
    .Y(_21_)
);

OAI21X1 _196_ (
    .A(N[3]),
    .B(_40_),
    .C(_47_),
    .Y(_48_)
);

FILL SFILL7120x8100 (
);

FILL SFILL6480x16100 (
);

OAI21X1 _120_ (
    .A(_111_[7]),
    .B(_95_),
    .C(state[3]),
    .Y(_96_)
);

FILL SFILL7120x10100 (
);

OAI21X1 _214_ (
    .A(_63_),
    .B(_62_),
    .C(_91_),
    .Y(_64_)
);

FILL SFILL19920x16100 (
);

BUFX2 _252_ (
    .A(_111_[4]),
    .Y(counter[4])
);

FILL SFILL20400x12100 (
);

NOR2X1 _117_ (
    .A(_111_[1]),
    .B(_111_[0]),
    .Y(_93_)
);

DFFSR _290_ (
    .Q(_114_[1]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(_3_[1])
);

AOI21X1 _155_ (
    .A(_17_),
    .B(_103_),
    .C(_18_),
    .Y(_2_[0])
);

OAI21X1 _193_ (
    .A(_45_),
    .B(_44_),
    .C(_91_),
    .Y(_46_)
);

BUFX2 _249_ (
    .A(_111_[1]),
    .Y(counter[1])
);

FILL FILL24080x12100 (
);

DFFSR _287_ (
    .Q(_111_[6]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_0_[6])
);

INVX1 _211_ (
    .A(_55_),
    .Y(_61_)
);

DFFSR _305_ (
    .Q(_113_[8]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_2_[8])
);

MUX2X1 _152_ (
    .A(_15_),
    .B(_16_),
    .S(_103_),
    .Y(_2_[8])
);

AOI21X1 _208_ (
    .A(_51_),
    .B(_39_),
    .C(_57_),
    .Y(_58_)
);

NAND2X1 _190_ (
    .A(_42_),
    .B(_36_),
    .Y(_43_)
);

INVX1 _246_ (
    .A(_88_),
    .Y(_5_)
);

FILL FILL23920x10100 (
);

DFFSR _284_ (
    .Q(_111_[3]),
    .CLK(clock_bF$buf1),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(_0_[3])
);

MUX2X1 _149_ (
    .A(_13_),
    .B(_14_),
    .S(_103_),
    .Y(_2_[7])
);

INVX2 _187_ (
    .A(_39_),
    .Y(_40_)
);

FILL SFILL19600x16100 (
);

FILL SFILL6480x14100 (
);

DFFSR _302_ (
    .Q(_113_[5]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_2_[5])
);

FILL SFILL19600x4100 (
);

AND2X2 _205_ (
    .A(_54_),
    .B(_55_),
    .Y(_56_)
);

FILL SFILL7600x10100 (
);

NAND3X1 _243_ (
    .A(_91_),
    .B(_89_),
    .C(_88_),
    .Y(_90_)
);

DFFSR _281_ (
    .Q(_111_[0]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_0_[0])
);

MUX2X1 _146_ (
    .A(_11_),
    .B(_12_),
    .S(_103_),
    .Y(_2_[6])
);

OAI21X1 _184_ (
    .A(_91_),
    .B(_34_),
    .C(_37_),
    .Y(_0_[0])
);

FILL FILL24080x10100 (
);

FILL SFILL18320x14100 (
);

DFFSR _278_ (
    .Q(state[4]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(state[2])
);

FILL SFILL6800x8100 (
);

NAND3X1 _202_ (
    .A(state[0]),
    .B(_52_),
    .C(_50_),
    .Y(_53_)
);

INVX1 _240_ (
    .A(_111_[7]),
    .Y(_87_)
);

FILL FILL23920x4100 (
);

MUX2X1 _143_ (
    .A(_9_),
    .B(_10_),
    .S(_103_),
    .Y(_2_[5])
);

AND2X2 _181_ (
    .A(_102__bF$buf3),
    .B(_111_[0]),
    .Y(_35_)
);

OAI21X1 _237_ (
    .A(N[7]),
    .B(_66_),
    .C(_83_),
    .Y(_84_)
);

FILL SFILL18960x8100 (
);

DFFSR _275_ (
    .Q(state[1]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(_6_)
);

NAND3X1 _178_ (
    .A(state[4]),
    .B(_102__bF$buf3),
    .C(_32_),
    .Y(_33_)
);

FILL SFILL7920x6100 (
);

FILL SFILL7120x4100 (
);

FILL SFILL6480x12100 (
);

MUX2X1 _140_ (
    .A(_109_),
    .B(_110_),
    .S(_103_),
    .Y(_2_[4])
);

AOI22X1 _234_ (
    .A(state[3]),
    .B(_80_),
    .C(_111_[6]),
    .D(_81_),
    .Y(_82_)
);

FILL SFILL19920x12100 (
);

BUFX2 _272_ (
    .A(_114_[6]),
    .Y(sr[6])
);

MUX2X1 _137_ (
    .A(_107_),
    .B(_108_),
    .S(_103_),
    .Y(_2_[3])
);

FILL SFILL19280x4100 (
);

AOI21X1 _175_ (
    .A(_102__bF$buf1),
    .B(_106_),
    .C(_30_),
    .Y(_3_[1])
);

BUFX2 _269_ (
    .A(_114_[3]),
    .Y(sr[3])
);

FILL SFILL18800x14100 (
);

NAND3X1 _231_ (
    .A(_70_),
    .B(_60_),
    .C(_78_),
    .Y(_79_)
);

FILL FILL23920x2100 (
);

MUX2X1 _134_ (
    .A(_105_),
    .B(_106_),
    .S(_103_),
    .Y(_2_[2])
);

OAI21X1 _172_ (
    .A(_114_[6]),
    .B(_102__bF$buf1),
    .C(_91_),
    .Y(_29_)
);

OAI21X1 _228_ (
    .A(_72_),
    .B(_73_),
    .C(_75_),
    .Y(_76_)
);

BUFX2 _266_ (
    .A(_114_[0]),
    .Y(sr[0])
);

FILL SFILL18960x6100 (
);

FILL SFILL18800x100 (
);

AOI21X1 _169_ (
    .A(_102__bF$buf0),
    .B(_12_),
    .C(_27_),
    .Y(_3_[5])
);

FILL SFILL7120x2100 (
);

FILL SFILL6960x12100 (
);

AOI21X1 _131_ (
    .A(_101_),
    .B(_103_),
    .C(_104_),
    .Y(_2_[1])
);

FILL FILL24080x8100 (
);

INVX1 _225_ (
    .A(_66_),
    .Y(_73_)
);

BUFX2 _263_ (
    .A(_113_[6]),
    .Y(dp[6])
);

INVX8 _128_ (
    .A(state[3]),
    .Y(_102_)
);

OAI21X1 _166_ (
    .A(_114_[3]),
    .B(_102__bF$buf2),
    .C(_91_),
    .Y(_26_)
);

DFFSR _298_ (
    .Q(_113_[1]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_2_[1])
);

BUFX2 BUFX2_insert10 (
    .A(_8_),
    .Y(_8__bF$buf3)
);

BUFX2 BUFX2_insert11 (
    .A(_8_),
    .Y(_8__bF$buf2)
);

BUFX2 BUFX2_insert12 (
    .A(_8_),
    .Y(_8__bF$buf1)
);

BUFX2 BUFX2_insert13 (
    .A(_8_),
    .Y(_8__bF$buf0)
);

FILL SFILL6800x4100 (
);

AOI21X1 _222_ (
    .A(_63_),
    .B(_70_),
    .C(state[0]),
    .Y(_71_)
);

BUFX2 _260_ (
    .A(_113_[3]),
    .Y(dp[3])
);

NOR2X1 _125_ (
    .A(startbuf[1]),
    .B(_99_),
    .Y(_100_)
);

AOI21X1 _163_ (
    .A(_102__bF$buf2),
    .B(_108_),
    .C(_24_),
    .Y(_3_[2])
);

NAND2X1 _219_ (
    .A(_66_),
    .B(_67_),
    .Y(_68_)
);

BUFX2 _257_ (
    .A(_113_[0]),
    .Y(dp[0])
);

FILL SFILL18480x8100 (
);

DFFSR _295_ (
    .Q(_114_[6]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf4),
    .S(vdd),
    .D(_3_[6])
);

OAI21X1 _198_ (
    .A(state[0]),
    .B(_49_),
    .C(_48_),
    .Y(_0_[2])
);

FILL SFILL18640x100 (
);

FILL SFILL7440x6100 (
);

INVX1 _122_ (
    .A(state[1]),
    .Y(_97_)
);

OAI21X1 _160_ (
    .A(state[3]),
    .B(_114_[0]),
    .C(_91_),
    .Y(_23_)
);

NOR2X1 _216_ (
    .A(N[5]),
    .B(N[6]),
    .Y(_65_)
);

BUFX2 _254_ (
    .A(_111_[6]),
    .Y(counter[6])
);

NAND3X1 _119_ (
    .A(_92_),
    .B(_93_),
    .C(_94_),
    .Y(_95_)
);

DFFSR _292_ (
    .Q(_114_[3]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_3_[3])
);

XNOR2X1 _157_ (
    .A(_114_[3]),
    .B(_114_[4]),
    .Y(_20_)
);

AOI21X1 _195_ (
    .A(_40_),
    .B(N[3]),
    .C(_91_),
    .Y(_47_)
);

DFFSR _289_ (
    .Q(_114_[0]),
    .CLK(clock_bF$buf4),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(_3_[0])
);

FILL SFILL18800x10100 (
);

FILL SFILL6800x2100 (
);

NOR2X1 _213_ (
    .A(_111_[4]),
    .B(_55_),
    .Y(_63_)
);

BUFX2 _251_ (
    .A(_111_[3]),
    .Y(counter[3])
);

NOR2X1 _116_ (
    .A(_111_[3]),
    .B(_111_[2]),
    .Y(_92_)
);

NOR2X1 _154_ (
    .A(N[0]),
    .B(_103_),
    .Y(_18_)
);

FILL SFILL20720x2100 (
);

NOR2X1 _192_ (
    .A(_42_),
    .B(_36_),
    .Y(_45_)
);

BUFX2 _248_ (
    .A(_111_[0]),
    .Y(counter[0])
);

DFFSR _286_ (
    .Q(_111_[5]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf0),
    .S(vdd),
    .D(_0_[5])
);

INVX1 _189_ (
    .A(_111_[1]),
    .Y(_42_)
);

INVX1 _210_ (
    .A(_111_[4]),
    .Y(_60_)
);

FILL SFILL18480x100 (
);

DFFSR _304_ (
    .Q(_113_[7]),
    .CLK(clock_bF$buf0),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_2_[7])
);

INVX1 _151_ (
    .A(_114_[7]),
    .Y(_16_)
);

INVX1 _207_ (
    .A(N[5]),
    .Y(_57_)
);

FILL FILL24080x4100 (
);

AND2X2 _245_ (
    .A(_100_),
    .B(state[1]),
    .Y(_4_)
);

DFFSR _283_ (
    .Q(_111_[2]),
    .CLK(clock_bF$buf1),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(_0_[2])
);

INVX1 _148_ (
    .A(_114_[6]),
    .Y(_14_)
);

NAND2X1 _186_ (
    .A(N[1]),
    .B(N[2]),
    .Y(_39_)
);

FILL SFILL18960x100 (
);

DFFSR _301_ (
    .Q(_113_[4]),
    .CLK(clock_bF$buf2),
    .R(_8__bF$buf3),
    .S(vdd),
    .D(_2_[4])
);

NAND3X1 _204_ (
    .A(state[3]),
    .B(_92_),
    .C(_93_),
    .Y(_55_)
);

OAI21X1 _242_ (
    .A(_102__bF$buf3),
    .B(_95_),
    .C(_111_[7]),
    .Y(_89_)
);

FILL SFILL20400x2100 (
);

DFFSR _280_ (
    .Q(startbuf[1]),
    .CLK(clock_bF$buf1),
    .R(_8__bF$buf2),
    .S(vdd),
    .D(startbuf[0])
);

INVX1 _145_ (
    .A(_114_[5]),
    .Y(_12_)
);

FILL SFILL6640x16100 (
);

OAI21X1 _183_ (
    .A(_36_),
    .B(_35_),
    .C(_91_),
    .Y(_37_)
);

NAND3X1 _239_ (
    .A(state[0]),
    .B(_84_),
    .C(_85_),
    .Y(_86_)
);

DFFSR _277_ (
    .Q(state[3]),
    .CLK(clock_bF$buf3),
    .R(_8__bF$buf1),
    .S(vdd),
    .D(_7_)
);

NAND2X1 _201_ (
    .A(_39_),
    .B(_51_),
    .Y(_52_)
);

FILL SFILL19120x6100 (
);

INVX1 _142_ (
    .A(_114_[4]),
    .Y(_10_)
);

FILL SFILL19440x4100 (
);

INVX1 _180_ (
    .A(N[1]),
    .Y(_34_)
);

INVX1 _236_ (
    .A(N[8]),
    .Y(_83_)
);

FILL FILL24080x2100 (
);

DFFSR _274_ (
    .Q(state[0]),
    .CLK(clock_bF$buf1),
    .R(vdd),
    .S(_8__bF$buf2),
    .D(_4_)
);

INVX1 _139_ (
    .A(_114_[3]),
    .Y(_110_)
);

INVX1 _177_ (
    .A(state[2]),
    .Y(_32_)
);

FILL SFILL6320x16100 (
);

FILL SFILL7280x10100 (
);

FILL SFILL18800x8100 (
);

FILL SFILL6640x8100 (
);

NAND3X1 _233_ (
    .A(_70_),
    .B(_60_),
    .C(_61_),
    .Y(_81_)
);

BUFX2 _271_ (
    .A(_114_[5]),
    .Y(sr[5])
);

INVX1 _136_ (
    .A(_114_[2]),
    .Y(_108_)
);

FILL SFILL6640x14100 (
);

OAI21X1 _174_ (
    .A(_114_[0]),
    .B(_102__bF$buf1),
    .C(_91_),
    .Y(_30_)
);

BUFX2 _268_ (
    .A(_114_[2]),
    .Y(sr[2])
);

CLKBUF1 CLKBUF1_insert0 (
    .A(clock),
    .Y(clock_bF$buf4)
);

CLKBUF1 CLKBUF1_insert1 (
    .A(clock),
    .Y(clock_bF$buf3)
);

CLKBUF1 CLKBUF1_insert2 (
    .A(clock),
    .Y(clock_bF$buf2)
);

CLKBUF1 CLKBUF1_insert3 (
    .A(clock),
    .Y(clock_bF$buf1)
);

CLKBUF1 CLKBUF1_insert4 (
    .A(clock),
    .Y(clock_bF$buf0)
);

FILL SFILL19120x10100 (
);

INVX1 _230_ (
    .A(_111_[6]),
    .Y(_78_)
);

FILL SFILL7760x6100 (
);

INVX1 _133_ (
    .A(_114_[1]),
    .Y(_106_)
);

AOI21X1 _171_ (
    .A(_102__bF$buf0),
    .B(_14_),
    .C(_28_),
    .Y(_3_[6])
);

INVX1 _227_ (
    .A(_74_),
    .Y(_75_)
);

BUFX2 _265_ (
    .A(_113_[8]),
    .Y(dp[8])
);

FILL SFILL19760x16100 (
);

endmodule
