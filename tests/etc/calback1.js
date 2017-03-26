var maxTime = 1000;

var evenDoubler = function(v, callback1){
    var waitTime = Math.floor(Math.random()*(maxTime+1));
    if (v%2) {
        setTimeout(function(){
            callback1(new Error("Odd input"));
        }, waitTime);
    } else {
        setTimeout(function(){
            callback1(null, v*2, waitTime);
        }, waitTime);
    }

};
module.exports.evenDoubler = evenDoubler;
module.exports.foo = "bar";
