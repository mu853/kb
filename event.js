chrome.runtime.onInstalled.addListener(function(){
    chrome.contextMenus.create({
        type: "normal",
        id: "wolken",
        title: "Wolkenを開く(ArticleId or Text)",
        contexts: ["all"]
    });

    chrome.contextMenus.create({
        type: "normal",
        id: "wolken-sr",
        title: "Wolkenを開く(SR)",
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

    chrome.contextMenus.create({
        type: "normal",
        id: "bugzilla",
        title: "bugzillaを開く",
        contexts: ["all"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    const text = info.selectionText;
    console.log(text);
    if (!text) {
        console.log("text not selected")
    } else {
        matches = text.match(/(KB|case|Case)?#?(\d{4,8})/)
        if (matches) {
            id = matches[2];
            console.log("KB number: " + id);
            switch (info.menuItemId) {
                case "wolken":
                    chrome.tabs.create({url: "https://broadcomcms-software-agent.wolkenservicedesk.com/wolken/esd/knowledge-base-view/view-kb-article?articleNumber=" + id + "&isLocationBackOnHome=true&hideTabs=true"});
                    break;
                case "wolken-sr":
                    chrome.tabs.create({url: "https://broadcomcms-software-agent.wolkenservicedesk.com/wolken/esd/case-view?caseId=" + id});
                    break;
                case "kb":
                    chrome.tabs.create({url: "https://knowledge.broadcom.com/external/article/" + id});
                    break;
                case "kb-legacy":
                    chrome.tabs.create({url: "https://knowledge.broadcom.com/external/article?legacyId=" + id});
                    break;
                case "bugzilla":
                    chrome.tabs.create({url: "https://bugzilla-vcf.lvn.broadcom.net/show_bug.cgi?id=" + id});
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

