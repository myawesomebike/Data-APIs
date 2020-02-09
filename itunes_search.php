<?

class itunesRequest {
	var $itRequestID = -1;
	var $country = "us";
	var $language = "en";
	var $itunesUserAgent = 'iTunes/12.0.1 (Macintosh; OS X 10.9.2) AppleWebKit/537.74.9';

	function itunesRequest($cc = '',$ll = '') {
		$storeCodes = dbPull("SELECT * FROM `country_codes` WHERE `code` = ?",array($cc));
		if($storeCodes[0]['itunes'] != '') {
			$this->maxSize = 10000000;
			$this->requestHeader = array(
				'User-agent' => $this->itunesUserAgent,
				'X-Apple-Tz' => '3600',
				'X-Apple-Store-Front' => $storeCodes[0]['itunes'] . '-1,12');
			$this->country = $cc;
			$this->language = $ll;
		}
	}
	function itunesSearch($searchTerm, $iPad = false) {
		$pieces = explode("%20",$searchTerm);
		$pieces = array_map("urlencode",$pieces);
		$encodedQuery = implode("+",$pieces);

		$params['term'] = $encodedQuery;
		if($iPad) {
			$params['entity'] = 'iPadSoftware';
		}
		$params['media'] = 'software';
		$params['country'] = $this->country;
		$params['language'] = $this->language . '_' . $this->country;
		$params['limit'] = 200;

		$requestURL = 'https://itunes.apple.com/search?' . $this->arrayToParams($params);
		$this->urlRequest($requestURL);
		$this->fetchURL();
		$doc = new DOMDocument();
		@$doc->loadHTML($this->body());

		$searchData = json_decode($this->body(),true);

		$rankData = array();
		foreach($searchData['results'] as $thisResult) {
			$thisData['id'] = $thisResult['trackId'];
			$thisData['name'] = $thisResult['trackName'];
			$thisData['description'] = $thisResult['description'];
			$thisData['rating'] = $thisResult['averageUserRatingForCurrentVersion'];
			$thisData['rating_count'] = $thisResult['userRatingCount'];
			$thisData['seller_name'] = $thisResult['sellerName'];
			$thisData['release_date'] = $thisResult['currentVersionReleaseDate']; //convert to timecode
			$thisData['version'] = $thisResult['version'];
			$thisData['genres'] = $thisResult['genres'];
			$thisData['price'] = $thisResult['price'];
			$rankData[] = $thisData;
		}
		return $rankData;
		
	}
	function getApp($appID) {
		$requestURL = 'https://itunes.apple.com/lookup?id=' . $appID;
		$uR = new urlRequest($requestURL);
		$uR->fetchURL($this->itunesUserAgent);
		$jData = json_decode($uR->body(),true);
		return $jData['results'][0];
	}
}
?>
