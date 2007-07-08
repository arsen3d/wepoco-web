package com.wepoco.apps.uploader;
/* A simple application using JetS3t to upload an image file to
 * the Amazon AWS S3 service.
 * Hardwired to upload image/png type files to the wepoco bucket,
 * but easily modified.
 */

import java.io.File;
import org.jets3t.service.S3Service;
import org.jets3t.service.acl.AccessControlList;
import org.jets3t.service.acl.GroupGrantee;
import org.jets3t.service.acl.Permission;
import org.jets3t.service.impl.rest.httpclient.RestS3Service;
import org.jets3t.service.model.S3Bucket;
import org.jets3t.service.model.S3Object;
import org.jets3t.service.security.AWSCredentials;

public class Upload {

		public static void uploadFile( S3Service s, S3Bucket b, AccessControlList acl, File data, String key ) throws Exception {
			S3Object fileObject = new S3Object(b, data);
			// S3 doesn't use directories/folders but keys can use '/' so it looks like
	        // there are directories.
			fileObject.setKey(key);
			// fileObject.setContentType("image/png");
	        fileObject.setAcl(acl);
	        // System.out.println("S3Object with data: " + fileObject);
	        s.putObject(b, fileObject);
		}

		public static void uploadDirectory( S3Service s, S3Bucket b, AccessControlList acl, File dir, String prefix ) throws Exception {
			if (dir.isDirectory()) {
	            String[] children = dir.list();
	            for (int i=0; i<children.length; i++) {
	                uploadDirectory(s, b, acl, new File(dir, children[i]), prefix + "/" + children[i]);
	            }
	        } else {
	        	// dir is a file and prefix is key
	        	uploadFile(s, b, acl, dir, prefix );
	        }
		}

	    public static void main( String[] args ) throws Exception {
	    	// If you have an account find keys here http://aws.amazon.com/
	    	String bucketName = System.getenv("AWS_BUCKET");
	    	if( bucketName == null ){
	    	  bucketName = "wepoco";
	    	}
	    	String awsAccessKey = System.getenv("AWS_ACCESS_KEY");
	    	if( awsAccessKey == null ){
	    		System.err.println("Please set env variables AWS_BUCKET, AWS_ACCESS_KEY and AWS_SECRET_KEY.");
	    		System.exit(1);
	    	}
	    	String awsSecretKey = System.getenv("AWS_SECRET_KEY");
	    	AWSCredentials credentials = new AWSCredentials(awsAccessKey, awsSecretKey);
	    	S3Service s3Service = new RestS3Service( credentials );
	    	S3Bucket[] myBuckets = s3Service.listAllBuckets();
	        //System.out.println("Searching buckets...");
	        S3Bucket wBucket = null;
	        for( int i=0; i<myBuckets.length; i++ ){
	        	//System.out.println("  " + myBuckets[i].getName());
	        	if( myBuckets[i].getName().equalsIgnoreCase( bucketName ) ){
	        		wBucket = myBuckets[i];
	        		//System.out.println( "Found chosen bucket!" );
	        	}
	        }
	        AccessControlList publicAcl = s3Service.getBucketAcl( wBucket );
	        publicAcl.grantPermission( GroupGrantee.ALL_USERS, Permission.PERMISSION_READ );
	        //System.out.println( "uploading " + args[0] + " as " + args[1] + " ..." );
	        File fileData = new File( args[0] );
	        if( fileData.isDirectory() ){
	        	uploadDirectory( s3Service, wBucket, publicAcl, fileData, args[1] );
	        }else{
	        	uploadFile( s3Service, wBucket, publicAcl, fileData, args[1] );
	        }
	    }
}