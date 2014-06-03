
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = window.innerWidth - margin.left - margin.right - 250,
    height = window.innerHeight - margin.top - margin.bottom - 50;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .3);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

var color = d3.scale.ordinal().range(['#FF6600', '#FFA366', '#C9C9C9', '#80CC80', '#009900']);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(d3.format(".2s"));

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right+250)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("plotdata_nonorm.csv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "language"; }));

  var normalized = true;

  data.forEach(function(d) {
    var y0 = 0;
    d.genders = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
    d.total = d.genders[d.genders.length - 1].y1;
  });

  data.sort(function(a, b) { return a['male'] - b['male']; }); 
  x.domain(data.map(function(d) { return d.language; }));
  y.domain([0, 100]);
  data.forEach(function(d) {
    d.genders.forEach(function(e){
      e.y0 = e.y0/d.total*100; 
      e.y1 = e.y1/d.total*100; 
      })
  })

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .attr("class", "y_label")
      .text("Percentage of repositories per category");
  
  var tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")
      .text("a simple tooltip");
  
  var language = svg.selectAll(".language")
      .data(data)
    .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x(d.language) + ",0)"; });
      
  language.selectAll("rect")
      .data(function(d) { return d.genders; })
    .enter().append("rect")
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.y1); })
      .attr("height", function(d) { return y(d.y0) - y(d.y1); })
      .style("fill", function(d) { return color(d.name); })
      .on("mouseover", function(d){
        current_rectangle_data = d3.select(this).datum();
        bar_data = d3.select(this.parentNode).datum();
        factor = normalized ? bar_data.total/100 : 1;
        tooltip.text(bar_data[current_rectangle_data.name]/factor);
        return tooltip.style("visibility", "visible");
      })
      .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");});


  var legend = svg.selectAll(".legend")
      .data(color.domain().slice().reverse())
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(150," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });

  legend.append("foreignObject")
      .attr("x", width-5)
      .attr("width", 100)
      .attr("height", 20)
      .append("xhtml:body")
      .html("<input type=radio name='sort_by'/>")
      .on("click", function (sort_cat) {
        if(normalized) {
            var x0 = x.domain(data.sort(function(a, b) { return a[sort_cat]/a.total - b[sort_cat]/b.total; }).map(function(d){ return d['language']; })).copy();
        } else {
          var x0 = x.domain(data.sort(function(a, b) { return a[sort_cat] - b[sort_cat]; }).map(function(d){ return d['language']; })).copy();
        }
        var transition = svg.transition().duration(750);

        language.transition().duration(750).attr("transform", function(d) { return "translate(" + x0(d.language) + ",0)"; });

        transition.select('.x.axis')
          .call(xAxis);
      });

    var normalizebox = svg.append("foreignObject")
      .attr("width", 100)
      .attr("height", 100)
      .attr("x", width + 50)
      .attr("y", height/2)
      .attr("text", "Raw Repo Counts")
      .html("<form><input type=checkbox><span>Raw Repo Counts</span></form>")
      .on("click", function(){
        if (!normalized) {
          y.domain([0, 100]);
          d3.select(".y_label").text("Percentage of repositories per category");
          data.forEach(function(d) {
            d.genders.forEach(function(e){
              e.y0 = e.y0/d.total*100; 
              e.y1 = e.y1/d.total*100; 
            })
          }) 
        } else {
          y.domain([0, d3.max(data, function(d) { return d.total; })]);
          d3.select(".y_label").text("Number of repositories per category");
          data.forEach(function(d) {
            d.genders.forEach(function(e){
              e.y0 = e.y0*d.total/100; 
              e.y1 = e.y1*d.total/100; 
            })
          }) 
        }

        normalized = !normalized;
        var transition = svg.transition().duration(750);

        transition.select('.y.axis')
          .call(yAxis);

        svg.selectAll(".language").data(data);

        language.selectAll("rect")
          .data(function(d) { return d.genders; })
          .transition().duration(750)
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("fill", function(d) { return color(d.name); });
      });

   normalizebox.append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .text("Raw Repo Counts");


});
