// Write a program that takes any number of command line arguments, all strings, and reverses them before outputting them one at a time to the console.
const args = process.argv;

const reverseStr = function(args) { 
  args.split("").reverse().join("");
}
reverseStr(args);