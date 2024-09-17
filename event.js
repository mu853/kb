chrome.runtime.onInstalled.addListener(function(){
    chrome.contextMenus.create({
        type: "normal",
        id: "wolken",
        title: "Wolkenを開く(ArticleId or Text)",
        contexts: ["all"]
    });

    chrome.contextMenus.create({
        type: "normal",
        id: "kb",
        title: "KBを開く(ArticleId or Text)",
        contexts: ["all"]
    });

    chrome.contextMenus.create({
        type: "normal",
        id: "kb-legacy",
        title: "KBを開く(LegacyId)",
        contexts: ["all"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    const text = info.selectionText;
    console.log(text);
    if (!text) {
        console.log("text not selected")
    } else {
        matches = text.match(/(KB|case|Case)?#?(\d{4,7})/)
        if (matches) {
            id = matches[2];
            console.log("KB number: " + id);
            switch (info.menuItemId) {
                case "wolken":
                    chrome.tabs.create({url: "https://broadcomcms-software-agent.wolkenservicedesk.com/wolken/esd/knowledge-base-view/view-kb-article?articleNumber=" + id + "&isLocationBackOnHome=true&hideTabs=true"});
                    break;
                case "kb":
                    chrome.tabs.create({url: "https://knowledge.broadcom.com/external/article/" + id});
                    break;
                case "kb-legacy":
                    chrome.tabs.create({url: "https://knowledge.broadcom.com/external/article?legacyId=" + id});
                    break;
                default:
                    //
            }
        } else {
            console.log("Search text: " + text);
            switch (info.menuItemId) {
                case "wolken":
                    chrome.tabs.create({url: "https://broadcomcms-software-agent.wolkenservicedesk.com/wolken/esd/kb_search?searchQuery=" + text});
                    break;
                default:
                    chrome.tabs.create({url: "https://support.broadcom.com/web/ecx/search?searchString=" + text});
            }
        }
    }
});
