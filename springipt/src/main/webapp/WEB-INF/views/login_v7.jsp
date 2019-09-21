<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>

<c:set var="contextPath" value="${pageContext.request.contextPath}"/>
<jsp:include page="base.jsp" />
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Log in to IPT</title>

   <!-- <link href="${contextPath}/resources/css/bootstrap.min.css" rel="stylesheet">
    <link href="${contextPath}/resources/css/common.css" rel="stylesheet">-->

</head>

<body>

<div class="container">

<div class="container-fluid" style="position: relative; z-index: 5;  
margin:-35px 0px 0px 0px; 
padding:45px 76px 35px 76px; 
text-align: left; 
font-size: 1.2em; 
background-color: #ffff80;
filter: alpha(opacity=50);
border-radius: 0px;">

<div class="col-md-12" style="margin-bottom: -25px">
        <div class="col-md-6" style="margin-left: -40px;width: 50%; margin-top: -40px">
    <h1 style="margin-top:7px;">What is IPT?</h1>
        <p>Interactive Parallelization Tool (IPT) is a semi-automatic tool that converts a C/C++ serial program into an efficient parallel program by parsing the specification by the users. It is currently being used for teaching parallel programming and supports MPI, OpenMP, and CUDA programming models.</p>

<p>
You can use IPT from the convenience of your web-browser. It is simple. Start by creating an account on this website or use your existing TACC portal account information.

</p>
		
		
    
    

<br><!--<p>Already joined? <a href="">Login Now!</a></p>--></div>
    <div style="margin-top: 15px" class="col-md-6"><p>If you login with your TACC portal account credentials, you will be also be able to compile and run the program generated by IPT on two XSEDE systems: Stampede2 and Comet.</p>
	
    <img src="https://www.tacc.utexas.edu/documents/1084364/1748789/stampede-boinc.jpg/" class="img-responsive" height="90%" width="90%">
    </div>
        </div>
</div>

<!-- /container -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="${contextPath}/resources/js/bootstrap.min.js"></script>
</body>
</html>
<jsp:include page="footer.jsp" />
	