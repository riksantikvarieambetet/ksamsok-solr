package se.raa.ksamsok.solr;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.solr.common.util.NamedList;

/**
 * Klass som bygger upp en datastruktur för att boosta data uifrån konf i solrconfig.xml för
 * se.raa.ksamsok.solr.TFBoostUpdateProcessorFactory. Exempel nedan som kopierar in itemLabel
 * och itemText 10 respektive 9 ggr till text, strict och item, och inkopiering av countyName
 * och provinceName 4 ggr var till text och strict.
 * 
 * 	    	<lst name="boost">
 *	      		<str name="tofields">text, strict, item</str>
 *	      		<lst name="from">
 *	      			<int name="itemLabel">10</int>
 *	      			<int name="itemTitle">9</int>	      			
 *	      		</lst>
 *	      	</lst>
 *	    	<lst name="boost">
 *	      		<str name="tofields">text, strict</str>
 *	      		<lst name="from">
 *	      			<int name="countyName">4</int>
 *	      			<int name="provinceName">4</int>
 *	      		</lst>
 *	      	</lst>
 */
class TFBoost {
	List<String> toFields = Collections.emptyList();
	Map<String, Integer> fromFieldTimes = Collections.emptyMap();

	@SuppressWarnings({ "rawtypes", "unchecked" })
	TFBoost(NamedList boost) {
		StringTokenizer tok = new StringTokenizer((String) boost.get("tofields"), ",");
		toFields = new ArrayList<String>(tok.countTokens());
		while (tok.hasMoreTokens()) {
			toFields.add(tok.nextToken().trim());
		}
		List<NamedList> fromFields = boost.getAll("from");
		if (fromFields != null) {
			fromFieldTimes = new LinkedHashMap<String, Integer>();
			for (NamedList from: fromFields) {
				for (int i = 0 ; i < from.size(); ++i) {
					String fromField = from.getName(i);
					Integer times = (Integer) from.getVal(i);
					fromFieldTimes.put(fromField, times);
				}
			}
		}
	}
	/**
	 * Ger lista med fält.
	 * @return lista med fältnamn, kan vara tom men aldrig null.
	 */
	List<String> getToFields() {
		return toFields;
	}
	/**
	 * Ger map med fältnamn och antal som nyckel respektive värde.
	 * @return map med fältnamn och antal, kan vara tom men aldrig null
	 */
	Map<String, Integer> getFromFieldTimes() {
		return fromFieldTimes;
	}
	/**
	 * Parsar och levererar en lista med boostningar enligt konf.
	 * @param args konf
	 * @return lista med boostningar, kan vara tom men aldrig null
	 */
	@SuppressWarnings({ "unchecked", "rawtypes" })
	static List<TFBoost> parseBoosts(NamedList args) {
		List<NamedList> boosts = args.getAll("boost");
		List<TFBoost> tfBoosts = Collections.emptyList(); 
		if (boosts != null) {
			tfBoosts = new ArrayList<TFBoost>(boosts.size());
			for (NamedList boost: boosts) {
				tfBoosts.add(new TFBoost(boost));
			}
		}
		return tfBoosts;
	}
}
