day = ARGS[1]
padded_day = lpad(day, 2, "0")

open("day" * padded_day * ".jl", "w") do file
    write(
        file,
        """
        # Read input
        open("./day$(padded_day).txt", "r") do file
            for line in eachline(file)
                println(line)
            end
        end
        """
    )
end