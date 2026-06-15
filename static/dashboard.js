// ---------- Risk Meter Animation ----------
function animateRiskBars(){

    const bars = document.querySelectorAll(".riskBar");

    bars.forEach(bar => {

        const value = bar.dataset.risk;
        bar.style.width = value + "%";

        if(value >= 80)
            bar.style.background="#ff2e63";
        else if(value >= 50)
            bar.style.background="#ff9f1c";
        else
            bar.style.background="#00ff9f";
    });
}

// ---------- Scan Animation ----------
function showScan(){

    const scan=document.getElementById("scanText");
    if(!scan) return;

    let dots=0;

    setInterval(()=>{
        dots=(dots+1)%4;
        scan.innerText="Scanning"+".".repeat(dots);
    },400);
}

window.onload=function(){
    animateRiskBars();
    showScan();
};