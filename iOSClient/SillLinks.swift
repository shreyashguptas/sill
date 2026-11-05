import Foundation

/// Where Sill sends people outside the app: this fork's addresses on the web, written once. FORK.md:
/// every address here is the fork's own GitHub repository, never upstream's website or its
/// App Store page; change `site` and the download, support and privacy links and the connect
/// screen's "Get it at …" all follow. Tests/checks/fork-hosts holds it to that.
enum SillLinks {
    /// The site. Its host is what the connect screen prints.
    static let site = URL(string: "https://github.com/shreyashguptas/sill")!
    /// Where the free Sill for Mac is downloaded (the connect screen's footer).
    static let download = site.appending(path: "releases")
    /// Help, and how to reach the developer, which guideline 1.5 wants inside the app as well as
    /// behind App Store Connect's Support URL (the connect screen's footer).
    static let support = site.appending(path: "issues")
    /// The privacy policy, which guideline 5.1.1(i) wants linked inside the app as well as in
    /// App Store Connect (the connect screen's footer).
    static let privacy = site.appending(path: "blob/main/site/privacy.html")
    /// The site as a person types it: "github.com/shreyashguptas/sill".
    static let siteName = (site.host() ?? "") + site.path

    /// Sill's App Store page, https://apps.apple.com/app/id‹Apple ID›: the link under a Mac's update
    /// notice (a goodbye "update"). The Apple ID is the App Store Connect record's, known once the
    /// record exists. This fork has no App Store record (FORK.md), so the placeholder stays and no
    /// link shows (the update notice's own words say what to do).
    static let appStoreText = "APP_STORE_URL_PLACEHOLDER"

    /// An https URL from `appStoreText`, else nil. DEBUG: `-SillAppStoreURL <url>` replaces it.
    static var appStore: URL? {
        #if DEBUG
        if let override = UserDefaults.standard.string(forKey: "SillAppStoreURL"), let url = https(override) { return url }
        #endif
        return https(appStoreText)
    }

    private static func https(_ text: String) -> URL? {
        guard let url = URL(string: text), url.scheme == "https", let host = url.host, !host.isEmpty else { return nil }
        return url
    }
}
