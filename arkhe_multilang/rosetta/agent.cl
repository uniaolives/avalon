__kernel void handover(__global int* counters, int sender_idx, int receiver_idx) {
    // Simulate atomic increment of receiver's counter
    atomic_inc(&counters[receiver_idx]);
}
