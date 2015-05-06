define(['jquery', './mdp', './graph', './data'], function ($, mdp, graph, data) {
  
  $('form.map-solve').on('submit', function(e){
    e.preventDefault();
    var mazeDesc = $(this).find('[name=maze]').val();
    mdp.solve(mazeDesc);
    $('.map-solve').hide();
    $('.secondary').show();
  });
  
  $('.back').on('click', function(e){
    $('.map-solve').show();
    $('.secondary').hide();
    data.set('simulation.running', false);
    data.set('update', true);
  });
  
  $('form.simulate').on('submit', function(e){
    e.preventDefault();
    var x = $(this).find('[name=posx]').val();
    var y = $(this).find('[name=posy]').val();
    if(x >= 0 && y >= 0 && x < data.get('matrix[0].length') && y < data.get('matrix.length') && data.get('matrix')[y][x]['val'] != null && Math.abs(data.get('matrix')[y][x]['val']) != 100){
//      mdp.move(x, y);
      data.set('simulation.running', true);
      data.set('simulation.y', y);
      data.set('simulation.x', x);
      data.set('update', true);
      window.setTimeout(mdp.move, 2000, data.get('simulation.x'), data.get('simulation.y'));
    } else {
      alert("Invalid position");
    }
    
  });
  
  document.body.appendChild(graph.view);
  graph.animate();

});