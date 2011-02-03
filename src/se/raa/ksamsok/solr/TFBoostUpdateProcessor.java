package se.raa.ksamsok.solr;

import java.io.IOException;
import java.util.List;
import java.util.Map;

import org.apache.solr.common.SolrInputDocument;
import org.apache.solr.update.AddUpdateCommand;
import org.apache.solr.update.processor.UpdateRequestProcessor;

/**
 * UpdateProcessor som boostar tf genom inkopiering av data vid add.
 */
class TFBoostUpdateProcessor extends UpdateRequestProcessor {

	private final TFBoostUpdateProcessorFactory tfBoostUpdateProcessorFactory;

	TFBoostUpdateProcessor(UpdateRequestProcessor next, TFBoostUpdateProcessorFactory tfBoostUpdateProcessorFactory) {
		super(next);
		this.tfBoostUpdateProcessorFactory = tfBoostUpdateProcessorFactory;
	}

	@Override
	public void processAdd(AddUpdateCommand cmd) throws IOException {
		SolrInputDocument doc = cmd.getSolrInputDocument();
		List<TFBoost> boosts = tfBoostUpdateProcessorFactory.getTfBoosts();
		for (TFBoost boost: boosts) {
			for (Map.Entry<String, Integer> fromFieldTime: boost.getFromFieldTimes().entrySet()) {
				String fromField = fromFieldTime.getKey();
				Integer times = fromFieldTime.getValue();
				Object fieldValue = doc.getFieldValue(fromField);
				if (fieldValue != null) {
					for (String toField: boost.getToFields()) {
						for (int i = 0; i < times; ++i) {
							doc.addField(toField, fieldValue);
						}
					}
				}
			}
		}
		super.processAdd(cmd);
	}
}
