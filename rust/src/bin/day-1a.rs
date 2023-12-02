fn main() -> std::io::Result<()> {
    let total: u32 = include_str!("../../../input/day-1.txt")
        .split("\n")
        .map(|x: &str| x.chars().filter(|x: &char| x.is_ascii_digit()).collect())
        .map(|x: Vec<char>| (x[0] as u32 - 48) * 10 + (*x.last().unwrap() as u32 - 48))
        .sum::<u32>();

    println!("{}", total);
    Ok(())
}
