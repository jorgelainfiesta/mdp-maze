define(['jquery', './data'], function ($, data) {
  //Stat connection and keep updating
  var solve = function(mazeDesc){
    $.ajax(data.get('opts.host') + "/solve", {data: {'maze' : mazeDesc}})
    .then(function(response){
      data.set('matrix', response);
      data.set('simulation.running', false);
      data.set('update', true);
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
    });
  };
  
  //Update function
  var counter = 0;
  
  var move = function(x, y){
    $.ajax(data.get('opts.host') + "/move", {data: {'x' : x, 'y' : y}})
    .then(function(response){
      data.set('simulation.running', true);
      data.set('simulation.y', response[0]);
      data.set('simulation.x', response[1]);
      data.set('update', true);
      var ncolor = (counter % 2 == 0) ? 0x3c64af : 0x3c85af;
      data.set('colors.simulate', ncolor);
      counter++;
      if(Math.abs(data.get('matrix')[response[0]][response[1]]['val']) != 100){
        window.setTimeout(move, 2000, data.get('simulation.x'), data.get('simulation.y'));
      } else {
        window.clearTimeout();
      }
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
      //Stop updating
      clearInterval();
    });
  };
  
  return {solve: solve, move: move};
});