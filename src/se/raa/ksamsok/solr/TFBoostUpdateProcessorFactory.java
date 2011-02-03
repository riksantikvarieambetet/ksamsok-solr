package se.raa.ksamsok.solr;

import java.util.Collections;
import java.util.List;

import org.apache.solr.common.util.NamedList;
import org.apache.solr.request.SolrQueryRequest;
import org.apache.solr.request.SolrQueryResponse;
import org.apache.solr.update.processor.UpdateRequestProcessor;
import org.apache.solr.update.processor.UpdateRequestProcessorFactory;

/**
 * UpdateProcessorFactory för att tillhandahålla termfrekvensboostning av fält till fritextindex
 * genom inkopiering av fältvärden.
 */
public class TFBoostUpdateProcessorFactory extends
		UpdateRequestProcessorFactory {
 
	List<TFBoost> tfBoosts = Collections.emptyList();

	@Override
	public UpdateRequestProcessor getInstance(SolrQueryRequest req,
			SolrQueryResponse res, UpdateRequestProcessor next) {
		return new TFBoostUpdateProcessor(next, this);
	}

	@SuppressWarnings("rawtypes")
	@Override
	public void init(final NamedList args) {
		super.init(args);
		if (args != null) {
			tfBoosts = TFBoost.parseBoosts(args);
		}
	}
	/**
	 * Ger lista med boosts.
	 * @return lista med boosts, kan vara tom men aldrig null.
	 */
	public List<TFBoost> getTfBoosts() {
		return tfBoosts;
	}
}

