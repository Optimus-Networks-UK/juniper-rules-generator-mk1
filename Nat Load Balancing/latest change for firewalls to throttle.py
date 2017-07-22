[edit]
+  class-of-service {
+      application-traffic-control {
+          rate-limiters 100meg {
+              bandwidth-limit 100024;
+              burst-size-limit 2000000;
+          }
+          rule-sets app-traffic-sch {
+              rule school_throttler {
+                  match {
+                      application-any;
+                  }
+                  then {
+                      rate-limit {
+                          client-to-server 100meg;
+                          server-to-client 100meg;
+                      }
+                  }
+              }
+          }
+      }
+  }
[edit security address-book global]
+    address WindowsUpdateInternet {
+        description "windows update on the internet.";
+        13.107.4.50/32;
+    }
     address ES-LIBITIV01 { ... }
[edit security address-book global]
+    address-set school_throttled_addresses {
+        address WindowsUpdateInternet;
+    }
    
[edit security policies from-zone DMZ666 to-zone U_OUTSIDE]
+     policy traffic_throttler {
+         match {
+             source-address [ ORANGE_Filters PEN_PROXIES ];
+             destination-address school_throttled_addresses;
+             application [ junos-http junos-https ];
+         }
+         then {
+             permit {
+                 application-services {
+                     application-traffic-control {
+                         rule-set app-traffic-sch;
+                     }
+                 }
+             }
+             log {
+                 session-init;
+             }
+         }
+         scheduler-name office-hours;
+     }
      policy Internet { ... }
[edit]
+  schedulers {                         
+      scheduler office-hours {
+          description "Office Hours";
+          monday {
+              start-time 07:00 stop-time 17:00;
+          }
+          tuesday {
+              start-time 07:00 stop-time 17:00;
+          }
+          wednesday {
+              start-time 07:00 stop-time 17:00;
+          }
+          thursday {
+              start-time 07:00 stop-time 17:00;
+          }
+          friday {
+              start-time 07:00 stop-time 17:00;
+          }
+      }
+  }