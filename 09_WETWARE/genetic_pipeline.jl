"""
Genetic Pipeline for Wetware
Variant library → RNA-seq → genAI → self-replication
"""

using Distributions
using Plots
using Random
using Statistics

# Types
struct Variant
    id::Int
    sequence::String
    expression::Float64
    fitness::Float64
    generation::Int
end

struct RNAseqSample
    variant_id::Int
    expression::Float64
    coverage::Int
end

struct MutationOperator
    rate::Float64
    effect_size::Float64
end

"""
Variant library with millions of sequences
"""
struct VariantLibrary
    variants::Dict{Int, Variant}
    next_id::Int
    generation::Int
end

VariantLibrary() = VariantLibrary(Dict{Int, Variant}(), 1, 1)

"""
Add a new variant to library
"""
function add_variant!(lib::VariantLibrary,
                     sequence::String,
                     expression::Float64,
                     fitness::Float64)
    variant = Variant(lib.next_id, sequence, expression, fitness, lib.generation)
    lib.variants[lib.next_id] = variant
    lib.next_id += 1
    return variant
end

"""
Simulate RNA-seq measurement
"""
function simulate_rnaseq(lib::VariantLibrary, coverage::Int=10000)
    # Expression levels determine sampling probability
    exprs = [v.expression for (_, v) in lib.variants]
    probs = exprs / sum(exprs)

    # Sample reads
    variant_ids = collect(keys(lib.variants))
    samples = sample(variant_ids, Weights(probs), coverage, replace=true)

    # Count reads per variant
    counts = Dict{Int, Int}()
    for id in samples
        counts[id] = get(counts, id, 0) + 1
    end

    # Create RNAseq samples
    rnaseq = RNAseqSample[]
    for (id, count) in counts
        exp = lib.variants[id].expression
        push!(rnaseq, RNAseqSample(id, exp, count))
    end

    return rnaseq
end

"""
genAI: generate new variants based on observed expression
Uses a simple Markov model trained on RNA-seq data
"""
function generate_new_variants(rnaseq::Vector{RNAseqSample},
                               n_new::Int=100,
                               mutation_rate::Float64=0.01)::Vector{String}

    # Extract sequences of highly expressed variants
    high_expr = filter(s -> s.expression > 0.5, rnaseq)
    if isempty(high_expr)
        # Fallback: random sequences
        return [randstring("ACGT", 100) for _ in 1:n_new]
    end

    # Learn transition probabilities (simplified)
    sequences = [string(i) for i in 1:length(high_expr)]  # dummy
    transition = ones(4, 4)  # ACGT -> ACGT

    # Generate new sequences
    new_seqs = []
    for _ in 1:n_new
        seq = []
        for pos in 1:100
            if !isempty(seq) && rand() < mutation_rate
                # Mutate
                push!(seq, rand("ACGT"))
            elseif isempty(seq)
                push!(seq, rand("ACGT"))
            else
                # Use transition from last base
                last_base = seq[end]
                idx = findfirst(isequal(last_base), "ACGT")
                probs = transition[idx, :] / sum(transition[idx, :])
                next_base = rand(["A","C","G","T"], Weights(probs))
                push!(seq, next_base)
            end
        end
        push!(new_seqs, join(seq))
    end
    return new_seqs
end

"""
Self-replication: library generates offspring
"""
function replicate!(lib::VariantLibrary,
                   rnaseq::Vector{RNAseqSample},
                   n_offspring::Int=100)

    new_sequences = generate_new_variants(rnaseq, n_offspring)
    lib.generation += 1

    for seq in new_sequences
        # Initial expression low, fitness based on seq length (dummy)
        expr = rand(Uniform(0.1, 0.3))
        fitness = 0.5 + 0.5 * rand()
        add_variant!(lib, seq, expr, fitness)
    end

    println("Generation $(lib.generation): added $(n_offspring) new variants")
    return lib
end

"""
Simulate evolution over multiple generations
"""
function simulate_evolution(n_generations::Int=10,
                           initial_size::Int=100,
                           selection_pressure::Float64=0.7)

    lib = VariantLibrary()

    # Initialize with random variants
    for i in 1:initial_size
        seq = randstring("ACGT", 100)
        expr = rand(Uniform(0.1, 1.0))
        fitness = rand()
        add_variant!(lib, seq, expr, fitness)
    end

    # Track metrics
    mean_expression = Float64[]
    library_size = Int[]

    for gen in 1:n_generations
        # RNA-seq
        rnaseq = simulate_rnaseq(lib)

        # Selection: keep only high expression
        exprs = [s.expression for s in rnaseq]
        if !isempty(exprs)
            push!(mean_expression, mean(exprs))
        end

        # Replication
        replicate!(lib, rnaseq)
        push!(library_size, length(lib.variants))
    end

    # Plot results
    p1 = plot(1:n_generations, mean_expression,
              xlabel="Generation", ylabel="Mean Expression",
              title="Evolution of Expression", legend=false)

    p2 = plot(1:n_generations, library_size,
              xlabel="Generation", ylabel="Library Size",
              title="Variant Library Growth", legend=false)

    plot(p1, p2, layout=(2,1))
    savefig("evolution_simulation.png")

    return lib
end

# Example usage
if abspath(PROGRAM_FILE) == @__FILE__
    println("Simulating genetic evolution...")
    simulate_evolution(10)
    println("Done. Plot saved to evolution_simulation.png")
end
