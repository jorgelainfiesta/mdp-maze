define(['pixi', './data', 'color'], function (PIXI, data, Color) {
  var container = new PIXI.Container(),
  numbers = new PIXI.Container(),
  arrows = new PIXI.Container(),
  size = 100,
  renderer = PIXI.autoDetectRenderer(data.get('opts.swidth'), data.get('opts.sheight'), {backgroundColor: data.get('colors.background')}),
  refreshMatrix = function(graphics, matrix) {
    if(data.get('update')){
      //Clear colors
      graphics.clear();
      //Remove old numbers
      for (var i = numbers.children.length - 1; i >= 0; i--) {
          numbers.removeChild(numbers.children[i]);
      };
      //Remove old arrows
      for (var i = arrows.children.length - 1; i >= 0; i--) {
          arrows.removeChild(arrows.children[i]);
      };
      
      var color;
      for (var i = 0; i < matrix.length; i++){
        for(var j = 0; j < matrix[0].length; j++){
          
          if(!matrix[i][j]['val']){
          //If it's a wall
            color = data.get('colors.wall');
          } else if(matrix[i][j]['val'] == 100 || matrix[i][j]['val'] == -100) {
          //If it's an absorbing state
            color = data.get('colors.absorbent');
            var richText = new PIXI.Text(matrix[i][j]['val'].toFixed(), {fill: data.get('text')});
            richText.x = size*j + 20;
            richText.y = size*i + 30;
            numbers.addChild(richText);
            
            if(data.get('simulation.running') && i == data.get('simulation.y') && j == data.get('simulation.x')){
              color = data.get('colors.simulate');
            }
          } else {
          //Otherwise, it's a normal state
            if(data.get('simulation.running')){
              if(i == data.get('simulation.y') && j == data.get('simulation.x')){
                color = data.get('colors.simulate');
                
              } else {
                color = 0xcccccc;
              }
              //Arrows
              var button;
              switch(matrix[i][j]['policy']){
                  case 'up' : button = new PIXI.Sprite(upButton); break;
                  case 'down' : button = new PIXI.Sprite(downButton); break;
                  case 'left' : button = new PIXI.Sprite(leftButton); break;
                  case 'right' : button = new PIXI.Sprite(rightButton); break;
              };
              button.x = size*j + 30;
              button.y = size*i + 30;
              arrows.addChild(button);
            } else {
              var pColor = Color("#b3d88e");
              color = "0x"+pColor.darken(matrix[i][j]['val'] * 0.5).toHex();
              var style = {fill: "#fff", opacity: 0.5};
              var richText = new PIXI.Text(matrix[i][j]['val'].toFixed(), style);
              richText.x = size*j + 10;
              richText.y = size*i + 10;
              numbers.addChild(richText);
              //Arrows
              var button;
              switch(matrix[i][j]['policy']){
                  case 'up' : button = new PIXI.Sprite(upButton); break;
                  case 'down' : button = new PIXI.Sprite(downButton); break;
                  case 'left' : button = new PIXI.Sprite(leftButton); break;
                  case 'right' : button = new PIXI.Sprite(rightButton); break;
              };
              button.x = size*j + 30;
              button.y = size*i + 45;
              arrows.addChild(button);
            }
          }
          graphics.beginFill(color, 1);
          graphics.drawRect(size*j, size*i, size, size);
          graphics.endFill();
          
        }
      }
      data.set('update', false);
    }
  },
  graphics = new PIXI.Graphics();
  //Add graphics to container
  container.addChild(graphics);
  container.addChild(numbers);
  container.addChild(arrows, 100);
  
  var upButton = PIXI.Texture.fromImage('images/up.png');
  var leftButton = PIXI.Texture.fromImage('images/left.png');
  var rightButton = PIXI.Texture.fromImage('images/right.png');
  var downButton = PIXI.Texture.fromImage('images/down.png');
  
  var animate = function() {
    requestAnimationFrame(animate);
    refreshMatrix(graphics, data.get('matrix'));
    renderer.render(container);
  };
  var clear = function(){
    
  };
  return {view: renderer.view, animate: animate};
});