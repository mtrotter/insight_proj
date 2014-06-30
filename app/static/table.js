var margin = { top: 50, right: 0, bottom: 100, left: 50 },
    width = 700- margin.left - margin.right,
    //height = 430 - margin.top - margin.bottom,
    height = 700 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 20),
    legendElementWidth = gridSize*2,
    buckets = 18,
    //colors =["#c82100","#c44100","#bf6000","#bb7d00","#b79800","#b3b300","#f9e235","#71aa00","#36a100","#009900"],
    //colors =["#003399", "003a9e","#0141A3","#0249a8","#0350ad","#0358b3","#045fb8","#0566bd","#066ec2","#0775c7","#077dcd","#0884d2","#098cd7","#0a93dc","#0b9ae1","0ba2e7","0ca9ec","0db1f1","0eb8f6",'0fc0fc'],
    //colors = ["ef1d0e","ea470e","e56f0e","e0960d","ef1d0e","ea470e","e56f0e","e0960d","dbbb0d","cdd50c",",a2d00c", "78cb0b", "51c60B","2bc10a","0abb0d","0ab62e","09b14e","09ac6b","08a787","08809c","07258d"]
    colors = ['#0013a8','#0029ad','#0141b2','#0259b7','#0372bc','#048cc1','#05a7c6','#06c3cb','#07d0c1','#08d6ad','#0adb98','#0be083','#0ce56c','#0eea55','#0fef3c','#10f423','#1bf912','#38ff14'],

days = amount_pred_str, //$
times = month_pred_str; //months
siteind = otherthing

if (siteind ==0){
  xlabe = "Campaign Description Length (words)";
  ylabe = "Number of Perks Offered";
}else {
  xlabe = "Campaign Description Length (words)";
  ylabe = "Campaign Duration (days)";
}

d3.tsv("/static/data.tsv", function(d) {
  return {
    day: +d.day,
    hour: +d.hour,
    value: +d.value
  };},
  function(error, data) {
    var colorScale = d3.scale.threshold()
      .domain([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,0.85, 0.9 ])
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
  .attr("x", function(d) { return ((d.hour - midpoint)/friendbin + gridxpad) * gridSize; })
  .attr("y", function(d) { return ((d.day - gridAmtSet*interval)/interval+4) * gridSize; })
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
    return d.hour == requested_repayment_term && d.day ==10*binreqLoanAmount;
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
    return "<h4> Funding Goal: $" + goal + "</h4><h4 >" + ylabe + ": " + d.day.toString()+ "<br>" + xlabe + ": " + d.hour.toString() + "  </h4> <h4 style = 'color :blue' > Funding Probability: " + d.value.toString()
                                                   })
                           })
d3.select("#chart").append("text")
    .attr("id","monthaxislabel")
    .text( xlabe)
    .style("position","absolute")
    .style("left","325px")
    .style("top","100px")
    .style("font-size","18px")
    .style("color", "black")
    .style("font-weight", "bold")

d3.select("svg").append("text")
    .attr("id","amountaxislabel")
    .text( ylabe)
    .style("position","relative")
    //.attr("style", "writing-mode: tb")
    .attr("transform", "translate(10,250)rotate(270)")
    //.style.transform("rotate(90deg)")
    //.style("left","500px")
    //.style("top","225px")
    .style("font-size","18px")
    .style("color", "black")
    .style("font-weight", "bold")
       ;
       
       
       
}); //end tsv
