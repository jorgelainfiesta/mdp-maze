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
  });
  
  document.body.appendChild(graph.view);
  graph.animate();

});