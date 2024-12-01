# Read input
raw = open("day01.txt", "r") do file
    readlines(file)
end

# Part 1
input = map(x -> map(x -> parse(Int, x), split(x, "   ")), raw)
input = hcat(input...)
left_list = input[1, :]
right_list = input[2, :]

sort!(left_list)
sort!(right_list)

total_distance = sum(abs.(left_list .- right_list))
println(total_distance)

# Part 2
count = Dict{Int,Int}()
for i in right_list
    count[i] = get(count, i, 0) + 1
end

similarity_score = sum(map(x -> x * get(count, x, 0), left_list))
println(similarity_score)