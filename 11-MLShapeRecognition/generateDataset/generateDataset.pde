void setup() {
  size(64, 64);
}

void draw() {
  for (int i = 0; i < 3; i++) {
    background(255);
    
    pushMatrix();

    float stroke = random(1, 6);
    float radius = random(8, 24);
    float angleSquare = random(0, 45);
    float angleTriangle = random(0,180);
    float xPos = random(radius, width-radius);
    float yPos = random(radius, height-radius);
    
    strokeWeight(2); // thickness
    stroke(0); // black
    translate(xPos, yPos); // position 
    
    if (i == 0) {
      circle(0, 0, radius*2);
      saveFrame("../data/circle####.png");
      
    } else if (i == 1) {
      rectMode(CENTER);
      rotate(angleSquare);
      square(0, 0, radius*2);
      saveFrame("../data/square####.png");
      
    } else if (i == 2) { 
      rotate(angleTriangle);
      triangle(0, -radius, radius, radius, -radius, radius);
      saveFrame("../data/triangle####.png");
    }
    
    popMatrix();
  }

  if (frameCount == 1000) {
    exit();
  }
}
