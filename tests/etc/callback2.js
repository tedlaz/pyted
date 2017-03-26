var mathfun = require('./calback1');
var  processResults = function(err, results, time){
    if (err){
        console.log("ERROR: " + err.message);
    } else {
        console.log("The reults are:" + results + " (" + time + " ms)");
    }
};

for (var i=0; i<10; i++){
    console.log("Calling evenDoubler with parameter " + i);
    mathfun.evenDoubler(i, processResults);
}
console.log("--------");
console.log("The foo variable :" + mathfun.foo);
