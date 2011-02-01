package se.raa.ksamsok.solr;

import java.io.File;
import java.text.NumberFormat;

import org.apache.solr.common.util.SimpleOrderedMap;
import org.apache.solr.core.SolrCore;
import org.apache.solr.handler.RequestHandlerBase;
import org.apache.solr.request.SolrQueryRequest;
import org.apache.solr.request.SolrQueryResponse;

/**
 * Simpel handler som hämtar hur stort indexet är på disk och hur mycket ledigt
 * utrymme det finns på den partitionen.
 */
public class IndexDiskInfoHandler extends RequestHandlerBase {

	@Override
	public String getDescription() {
		return "Get index and disk info";
	}

	@Override
	public String getSource() {
		return "N/A";
	}

	@Override
	public String getSourceId() {
		return "$Id: IndexDiskInfoHandler.java,v 1.1 2011/02/01 10:52:32 niklas Exp $";
	}

	@Override
	public String getVersion() {
		return "$Revision: 1.1 $";
	}

	@Override
	public void handleRequestBody(SolrQueryRequest req, SolrQueryResponse res)
			throws Exception {
		SimpleOrderedMap<Object> dirs = new SimpleOrderedMap<Object>();
		SolrCore core = req.getCore();

		File indexDir = new File(core.getIndexDir());
		dirs.add("path", indexDir.getAbsolutePath());
		dirs.add("free", readableSize(indexDir.getUsableSpace()));
		dirs.add("size", readableSize(computeIndexSize(indexDir)));
		res.add( "index", dirs ); 
		res.setHttpCaching(false);
	}

	private String readableSize(long size) {
	    NumberFormat formatter = NumberFormat.getNumberInstance();
	    formatter.setMaximumFractionDigits(2);
	    if (size / (1024 * 1024 * 1024) > 0) {
	      return formatter.format(size * 1.0d / (1024 * 1024 * 1024)) + " GB";
	    } else if (size / (1024 * 1024) > 0) {
	      return formatter.format(size * 1.0d / (1024 * 1024)) + " MB";
	    } else if (size / 1024 > 0) {
	      return formatter.format(size * 1.0d / 1024) + " KB";
	    } else {
	      return String.valueOf(size) + " bytes";
	    }
	  }

	private long computeIndexSize(File f) {
		if (f.isFile()) {
		 	return f.length();
		}
	 	File[] files = f.listFiles();
	 	long size = 0;
	 	if (files != null && files.length > 0) {
	 		for (File file : files) {
	 			size += file.length();
	 		}
	 	}
	 	return size;
	 } 
}
