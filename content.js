//document.getElementByXPath = function(sValue) { var a = this.evaluate(sValue, this, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null); if (a.snapshotLength > 0) { return a.snapshotItem(0); } };
//document.getElementsByXPath = function(sValue){ var aResult = new Array();var a = this.evaluate(sValue, this, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);for ( var i = 0 ; i < a.snapshotLength ; i++ ){aResult.push(a.snapshotItem(i));}return aResult;};

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

const toolbar = getElementByXpath("//html/body/e-root");
//const toolbar = getElementByXpath("//html[1]/body[1]/e-root[1]/e-esd[1]/e-frame-layout[1]/div/e-header[1]/mat-toolbar[1]/div[1]/div[3]/div[2]");
if(toolbar){
    console.log(toolbar.innerHTML);
    console.log(toolbar);
}else{
    console.log("toolbar not found");
}

/*
<div _ngcontent-llw-c987="" fxlayout="row" fxlayoutalign="end center" fxlayoutgap="1rem" style="flex-direction: row; box-sizing: border-box; display: flex; place-content: center flex-end; align-items: center;">
    <div _ngcontent-llw-c987="" class="header-create-case-btn add-icon-create" style="margin-right: 1rem;">
        <button _ngcontent-llw-c987="" color="primary" mat-button="" class="mat-focus-indicator new-case mat-button mat-button-base mat-primary ng-star-inserted">
            <span class="mat-button-wrapper">
                <div _ngcontent-llw-c987="" fxlayout="row" fxlayoutalign="center center" fxlayoutgap="4px" style="flex-direction: row; box-sizing: border-box; display: flex; place-content: center; align-items: center;">
                    <span _ngcontent-llw-c987="">Save Case</span>
                </div>
            </span>
            <span matripple="" class="mat-ripple mat-button-ripple"></span>
            <span class="mat-button-focus-overlay"></span>
        </button>
    </div>


mat-toolbar > div > div(3つ目) > div(2つ目) ここの先頭にdivを追加する
*/
