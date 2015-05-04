define(['pixi', './data', 'color'], function (PIXI, data, Color) {
  var container = new PIXI.Container(),
  size = 100,
  renderer = PIXI.autoDetectRenderer(data.get('opts.swidth'), data.get('opts.sheight'), {backgroundColor: data.get('colors.wall')}),
  refreshMatrix = function(graphics, matrix) {
    graphics.clear();
    var color = 0xffffff;
    for (var i = 0; i < matrix.length; i++){
      for(var j = 0; j < matrix[0].length; j++){
        if(!matrix[i][j]['val']){
          color = 0x000000;
        } else {
          var pColor = Color("#ffff00");
          color = "0x"+pColor.darken(matrix[i][j]['val'] * 0.4).toHex();
          var richText = new PIXI.Text(matrix[i][j]['val'].toFixed(0));
          richText.x = size*j + 10;
          richText.y = size*i + 10;
          container.addChild(richText);
        }
        graphics.beginFill(color, 1);
        graphics.drawRect(size*j, size*i, size, size);
        graphics.endFill();
      }
    }
  },
  graphics = new PIXI.Graphics();
  //Add graphics to container
  container.addChild(graphics);

  var animate = function() {
      requestAnimationFrame(animate);
      refreshMatrix(graphics, data.get('matrix'));
      renderer.render(container);
  }
  return {view: renderer.view, animate: animate};
});