# Read input
raw = open("day02.txt", "r") do file
    readlines(file)
end

# Part 1
safe = 0
for report in raw
    levels = map(x -> parse(Int, x), split(report, " "))
    diff = levels[2] - levels[1]
    increasing = levels[2] - levels[1] > 0 ? true : false
    if !(1 <= abs(diff) <= 3)
        continue
    end

    global safe += 1
    for i in 2:length(levels)-1
        diff = levels[i+1] - levels[i]

        if !((!increasing && -3 <= diff <= -1) || (increasing && 1 <= diff <= 3))
            global safe -= 1
            break
        end
    end
end

println(safe)

# Part 2
safe = 0
for report in raw
    levels = map(x -> parse(Int, x), split(report, " "))
    diff = levels[2] - levels[1]
    increasing = levels[2] - levels[1] > 0 ? true : false
    if !(1 <= abs(diff) <= 3)
        continue
    end

    global safe += 1
    for i in 2:length(levels)-1
        diff = levels[i+1] - levels[i]

        if !((!increasing && -3 <= diff <= -1) || (increasing && 1 <= diff <= 3))
            global safe -= 1
            break
        end
    end
end

println(safe)
