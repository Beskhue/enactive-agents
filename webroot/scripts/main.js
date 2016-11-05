var TRACES_FILE = "data/traces.json";

var doTraces = (function () {
    var prevData = null;
    return function() { 
        $.ajax({
            url: TRACES_FILE,
            dataType: "text"
        }).done(function(data) {
            if(prevData && prevData == data) {
                return;
            }
            prevData = data;
            data = $.parseJSON(data);
            
            var tracesContainer = $("#traces");
            tracesContainer.empty();
            
            for(agent in data) {
                agentHistory = data[agent];
                var div = $("<div>");
                var traces = $("<div>").addClass('traces');
                div.append($("<p>").text(agent));
                div.append(traces);
                
                for(var i = 0; i < agentHistory["enaction"].length; i++) {
                    var interactionValence = agentHistory["enaction"][i];
                    var interaction = interactionValence[0];
                    if(interaction.interaction) {
                        interaction = interaction.interaction
                    }
                    var valence = interactionValence[1];
                    traces.append(" ");
                    switch(interaction.name) {
                        case "Step":
                            if(interaction.result == "Succeed") {
                                traces.append("&#x2192;");
                            } else {
                                traces.append("&#x21DD;");
                            }
                            break;
                        case "Turn Left":
                            traces.append("&#x2B0F;");
                            break;
                        case "Turn Right":
                            traces.append("&#x21B4;");
                            break;
                        case "Feel":
                            if(interaction.result == "Succeed") {
                                traces.append("&#x25A0;");
                            } else {
                                traces.append("&#x25A1;");
                            }
                            break;
                        default:
                            traces.append("?");
                    }
                }
                
                tracesContainer.append(div);
            }
        }).always(function() { 
            setTimeout(function() { doTraces(); }, 100);
        });
    };
})();

(function() {
    // Main entry-point function
    doTraces();
})();

hashCode = function(s){
  return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);              
}

