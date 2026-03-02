# multi-language/julia/ucd.jl
using Statistics

function verify_conservation(C, F; tol=1e-10)
    return abs(C + F - 1.0) < tol
end

struct UCD
    data::Matrix{Float64}
end

function analyze(ucd::UCD)
    n = size(ucd.data, 1)
    if n > 1
        corr_mat = abs.(cor(ucd.data'))
        C = (sum(corr_mat) - n) / (n * (n - 1))
    else
        C = 0.5
    end
    F = 1.0 - C
    return (C=C, F=F, conservation=verify_conservation(C, F))
end

# Example
data = [1.0 2.0 3.0 4.0; 2.0 3.0 4.0 5.0; 5.0 6.0 7.0 8.0]
ucd = UCD(data)
println(analyze(ucd))
