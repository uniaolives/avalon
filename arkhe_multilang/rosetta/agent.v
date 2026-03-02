module agent (
    input clk,
    input rst,
    input send_en,
    output reg [7:0] counter
);
    always @(posedge clk) begin
        if (rst)
            counter <= 0;
        else if (send_en)
            counter <= counter + 1;
    end
endmodule

module handover (
    input clk,
    input alice_send,
    output wire [7:0] bob_counter
);
    agent alice (.clk(clk), .rst(1'b0), .send_en(alice_send), .counter());
    agent bob   (.clk(clk), .rst(1'b0), .send_en(alice_send), .counter(bob_counter));
endmodule
