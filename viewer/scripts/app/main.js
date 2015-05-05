define(['jquery', './mdp', './graph', './data'], function ($, mdp, graph, data) {
  
  $('form.map-solve').on('submit', function(e){
    e.preventDefault();
    var mazeDesc = $(this).find('[name=maze]').val();
    mdp.solve(mazeDesc);
  });
  
  document.body.appendChild(graph.view);
  graph.animate();

});