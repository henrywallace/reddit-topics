$(function() { // DOM Ready

  // CY Styling
  var cy = cytoscape({
    container: document.getElementById('cy'),

    style: cytoscape.stylesheet()
    .selector('node')
    .css({
      'content': 'data(name)',
      //'text-valign': 'center',
      'color': 'white',
      'text-outline-width': 2,
      'text-outline-color': '#888',
      'background-color': 'blue',
    })
    .selector('edge')
    .css({
      'target-arrow-shape': 'triangle',
      'width': 'mapData(weight,0,1,1,6)',
    }),

    elements: testjson, // object defined in external file, ugh.

    layout: {
      name: 'cose',
      padding: 10
    }
  });

  // Edge Removal via Slider
  var to_remove = 0;

  $('#slider').slider({
    change: function(event, ui) { // triggers when slider moved
      var slide_value = ui.value/100;
      console.log(slide_value);


      var text_val = Math.floor((1-slide_value)*100);
      $("#slider_val").text("The top "+text_val+"% of edges between topics are shown."); // fill in value in html page

      if( to_remove != 0){
        // if we aren't in the initial case... put all edges back before we remove them again.
        to_remove.restore();
      }

      to_remove = cy.elements('edge[weight < '+slide_value+'][type = "topic"]');
      // removes edges from TOPICS. Edges between words untouched.

      cy.remove(to_remove);
    }
  });

}); // on dom ready
