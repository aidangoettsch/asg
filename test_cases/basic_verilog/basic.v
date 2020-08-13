module medium (
    input a,
    input b,
    input c,
    input d,
    output o
);
    wire vdd = 1'b1;
    wire gnd = 1'b0;

    assign o = (~a & ~b) ^ (c | d);
endmodule
