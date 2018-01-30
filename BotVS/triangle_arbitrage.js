// cancel all orders
function CancelPendingOrders() {
    for(var e in exchanges){
        var orders = _C(exchanges[e].GetOrders);
        for (var j = 0; j < orders.length; j++) {
          exchanges[e].CancelOrder(orders[j].Id, orders[j]);}
    }
}

function BuyAll(Price, Symbol){
    Symbol.Buy(Price, _N(Symbol.GetAccount().Stocks * 0.9, 3));
}

function SellAll(Price, Symbol){
    Symbol.Sell(Price, _N(Symbol.GetAccount().Stocks * 0.9, 3));
}

function onTick() {
    if(exchanges.length != 3){
        throw("Only three exchanges are supported");
    }

    var P1_SELL = exchanges[0].GetTicker().Sell;
    var P1_BUY = exchanges[0].GetTicker().Buy;
    var P2_SELL = exchanges[1].GetTicker().Sell;
    var P2_BUY = exchanges[1].GetTicker().Buy;
    var P3_SELL = exchanges[2].GetTicker().Sell;
    var P3_BUY = exchanges[2].GetTicker().Buy;
    // use the if-structure to decide the arbitrage direction
    if ((P2_SELL/P3_BUY - P1_BUY) / (P2_SELL/P3_BUY) >= threshold) {
        // policy 1
        Log("利润空间: "+(P2_SELL/P3_BUY - P1_BUY) / (P2_SELL/P3_BUY));
        CancelPendingOrders();
        SellAll(P2_SELL, exchanges[1]);
        BuyAll(P3_BUY, exchanges[2]);
        BuyAll(P1_BUY, exchanges[0]);
        Log("正三角套利完成! ");
    }
    if ((P1_SELL - P2_BUY/P3_SELL) / P1_SELL >= threshold){
        // policy 2
        Log("利润空间:"+(P1_SELL - P2_BUY/P3_SELL) / P1_SELL);
        CancelPendingOrders();
        SellAll(P1_SELL, exchanges[0]);
        SellAll(P3_SELL, exchanges[2]);
        BuyAll(P2_BUY, exchanges[1]);
        Log("逆三角套利完成! ");
    }
}

function main() {
    while (true) {
        onTick();
        Sleep(sleeptime);
    }
}