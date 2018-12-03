var userGUISettingsSessionStorageKey = "userGUISettings";

function refreshUserGUISettings(apiURL) {
    $.ajax({
        url: apiURL,
        dataType: "json"
    }).done(function(data) {
        console.log("userGUISettings refreshed successfully");
        sessionStorage.setItem(userGUISettingsSessionStorageKey, JSON.stringify(data));
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log("userGUISettings refresh failed: " + errorThrown);
    });
}

function getUserGUISettingsAttribute(key) {
    var userGUISettings = JSON.parse(sessionStorage.getItem(userGUISettingsSessionStorageKey));
    return userGUISettings[key];
}

function flushUserGUISettings() {
    sessionStorage.removeItem(userGUISettingsSessionStorageKey);
}
