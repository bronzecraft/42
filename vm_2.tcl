proc masspointcreate {} {
	set em123 [hm_getmass comps 1]
	set em [lindex $em123 0]
	global em_xyz nodeid compname
	# puts $em_xyz
	# *deletemark elements 1
	set em_name [expr int($em)]
	set _1 _1
	set em_name mass$em_name
	set em_m $em_name
	set mass _mass
	#########################create a new property
	set n 1
	*createentity props cardimage="MASS" name=$compname$mass
	*setvalue props name=$compname$mass STATUS=1 461=$em
	####################### create a new components
	*createentity comps name=$compname$mass
	*createmark props 1 "by prop name" $compname$mass
	set propid [hm_getmark props 1]
	*setvalue comps name=$compname$mass propertyid=$propid
	*createmark nodes 1 $nodeid
	########################### create a new mass element
	*masselement 1 0 "$compname$mass" 0
	}
# define a rom property 
proc rotaty {} {
	global em_xyz nodeid  compid rm123
	set compname [clock seconds]
	*createmark comps 1 $compid
	set r468 [lindex $rm123 0]
	set r469 [lindex $rm123 1]
	set r470 [lindex $rm123 2]
	set r471 [lindex $rm123 3]
	set r472 [lindex $rm123 4]
	set r473 [lindex $rm123 5]
	set rota _rota
	*clearmark props 1
	*createentity props cardimage="ROTARY_INERTIA" name=$rota$compname
	*createmarklast props 1
	set propid [hm_getmark props 1]
	*setvalue props id=$propid STATUS=1 468=$r468
	*setvalue props id=$propid STATUS=1 469=$r469
	*setvalue props id=$propid STATUS=1 470=$r470
	*setvalue props id=$propid STATUS=1 299=$r471
	*setvalue props id=$propid STATUS=1 300=$r472
	*setvalue props id=$propid STATUS=1 301=$r473
	*clearmark comps 1
	# puts 11111
	*createentity comps name=$rota$compname
	*createmarklast comps 1
	set comnpid [hm_getmark comps 1]
	*setvalue comps id=$comnpid propertyid=$propid
	*clearmark nodes 1
	*createmark nodes 1 $nodeid
	# *createnode [lindex $em_xyz 0] [lindex $em_xyz 1] [lindex $em_xyz 2]
	# *createmarklast nodes 1
	set propname [hm_getvalue props id=$propid dataname=name]
	*masselement 1 0 "$propname" 0
	*elementtype 1 2
	*createmarklast elements 1 
	*elementsettypes 1
	*elementtype 1 1
	}
# erase density of the material
proc erasdensity {compid compname} {
	 
	# global compid compname
	# puts $compid
	set propid [hm_getvalue comps id=$compid dataname=propertyid]
	set matid [hm_getvalue properties id=$propid dataname=materialid]
	set erd _erd
	*clearmark props 1
	*createentitysameas props $propid
	*createmarklast props 1
	*clearmark mat 1
	catch {*createentitysameas mat $matid }
	*createmarklast mat 1
	*clearmark comps 1
	*createmarklast comps 1
	# set compnid [hm_getmark comps 1]
	set propid [hm_getmark props 1]
	set matid [hm_getmark mats 1]
	*setvalue mats id=$matid name=$compname$erd 
	set newDensity [hm_getvalue materials id=$matid dataname=Density]
	set newDensity [expr $newDensity/1000.0]
	*setvalue props id=$propid materialid=$matid
	*setvalue props id=$propid name=$compname$erd
	*setvalue comps id=$compid propertyid=$propid
	*setvalue comps id=$compid name=$compname$erd
	*setvalue mats id=$matid Density=$newDensity
	}
	

*clearmark elems 1
*clearmark nodes 1
*createmarkpanel comps 1 "please select comps"
set len_comp [hm_getmark comps 1] 
set len_c [llength $len_comp]
if { $len_c<2} {
	set em_xyz [hm_getcog comps 1]
	set rm123 [hm_getmoi comps 1 1]
	set compid [hm_getmark comps 1]
	set compname [hm_getvalue comps id=$compid dataname=name]
	set compname N$compname
	*clearmark nodes 1
	*createnode [lindex $em_xyz 0] [lindex $em_xyz 1] [lindex $em_xyz 2]
	*createmarklast nodes 1
	set nodeid [hm_getmark nodes 1]
	masspointcreate
	rotaty
	erasdensity $compid $compname
	unset em_xyz compid compname nodeid
	} else {
########################################
	set em_xyz [hm_getcog comps 1]
	set rm123 [hm_getmoi comps 1 1]
	
	set compid [hm_getmark comps 1]
	set compname [clock seconds]
	*clearmark nodes 1
	*createnode [lindex $em_xyz 0] [lindex $em_xyz 1] [lindex $em_xyz 2]
	*createmarklast nodes 1
	set nodeid [hm_getmark nodes 1]
	rotaty
	masspointcreate
	foreach cid $compid {
	set cname [hm_getvalue comps id=$cid dataname=name]
	erasdensity $cid $cname
	}	

puts 1}

*clearmark elems 1
*clearmark nodes 1