module basic (
    inout vdd,
    inout gnd,
    input a,
    output o
);
    assign o =~a;
endmodule
