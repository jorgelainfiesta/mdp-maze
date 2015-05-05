define(['jquery', './data'], function ($, data) {
  //Stat connection and keep updating
  var solve = function(mazeDesc){
    $.ajax(data.get('opts.host') + "/solve", {data: {'maze' : mazeDesc}})
    .then(function(response){
      data.set('matrix', response);
//        console.log(response);
      data.set('update', true);
      //Start updating each 300ms
//      setInterval(update, data.get('opts.interval'));
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
    });
  };
  
  //Update function
  var update = function(){
    $.ajax(data.get('opts.host') + "/update")
    .then(function(response){
      data.set('matrix', JSON.parse(response));
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
      //Stop updating
      clearInterval();
    });
  };
  
  return {solve: solve};
});