var margin = { top: 50, right: 0, bottom: 100, left: 50 },
    width = 700- margin.left - margin.right,
    //height = 430 - margin.top - margin.bottom,
    height = 700 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 20),
    legendElementWidth = gridSize*2,
    buckets = 9,
    colors =["#c82100","#c44100","#bf6000","#bb7d00","b79800","#b3b300","91ae00","#71aa00","#36a100","#009900"],



days = amount_pred_str, //$
times = month_pred_str; //months

d3.tsv("/static/data.tsv", function(d) {
  return {
    day: +d.day,
    hour: +d.hour,
    value: +d.value
  };},
  function(error, data) {
    var colorScale = d3.scale.threshold()
      .domain([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ])
      .range([0].concat(colors));

    var svg = d3.select("#chart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var dayLabels = svg.selectAll(".dayLabel")
  .data(days)
  .enter().append("text")
  .text(function (d) { return d; })
  .attr("x", 0)
  .attr("y", function (d, i) { return i * gridSize; })
  .style("text-anchor", "end")
  .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
  .attr("class", function (d, i) { return ((i >= 0 ) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

var timeLabels = svg.selectAll(".timeLabel")
  .data(times)
  .enter().append("text")
  .text(function(d) { return d; })
  .attr("x", function(d, i) { return i * gridSize; })
  .attr("y", 0)
  .style("text-anchor", "middle")
  .attr("transform", "translate(" + gridSize / 2 + ", -6)")
  .attr("class", function(d, i) { return ((i >= 0) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });


var heatMap = svg.selectAll(".hour")
  .data(data)
  .enter().append("rect")
  .attr("x", function(d) { return (d.hour - requested_repayment_term+100)/10 * gridSize; })
  .attr("y", function(d) { return (d.day/100 - gridAmtSet+5) * gridSize; })
  .attr("rx", 4)
  .attr("ry", 4)
  .attr("class", "hour bordered")
  .attr("width", gridSize)
  .attr("height", gridSize)
  .style("fill", colors[0]);


heatMap.transition().duration(1000)
  .style("fill", function(d) { return colorScale(d.value); });



d3.selectAll("rect.bordered")
  .classed("target", function(d) {
    return d.hour == requested_repayment_term && d.day ==100*binreqLoanAmount;
  })
       
console.log(requested_repayment_term)
console.log(roundedReqAmt)
console.log(binreqLoanAmount)

       
d3.select("#chart").append("text")
  .attr("id","fund")
  .text( " ")
  .style("position","absolute")
  .style("left","820px")
  .style("top","300px")
  .style("font-size","18px")
  .style("color", "blue")
  .style("font-weight", "bold")

s = d3.selectAll("rect").on("mouseover",function(d){
    d3.select("#fund").html(function(){
    return "<h4 > Funding Goal: $" + d.day.toString()+ "<br> Number of Facebook Friends: " + d.hour.toString() + "  </h4> <h4 style = 'color :blue' > Funding Probability: " + d.value.toString()
                                                   })
                           })
d3.select("#chart").append("text")
    .attr("id","monthaxislabel")
    .text( " Number of Facebook Friends")
    .style("position","absolute")
    .style("left","325px")
    .style("top","100px")
    .style("font-size","16px")
    .style("color", "black")
    .style("font-weight", "bold")

d3.select("svg").append("text")
    .attr("id","amountaxislabel")
    .text( " Funding Goal ($)")
    .style("position","absolute")
    //.attr("style", "writing-mode: tb")
    .attr("transform", "translate(10,250)rotate(270)")
    //.style.transform("rotate(90deg)")
    //.style("left","25px")
    //.style("top","225px")
    .style("font-size","16px")
    .style("color", "black")
    .style("font-weight", "bold")
       ;
       
       
       
}); //end tsv
