// 
function sum(nums){
    let total = 0

    for(let num of nums){
        total += num
    }
    return total
}
function find_mean(array){
    // sum all numbers
    const total = sum(array)

    return total / array.length
}
const pi = 3.142
export {pi, sum};
export default find_mean