<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>

<c:set var="contextPath" value="${pageContext.request.contextPath}" />
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Interactive Parallelization Tool</title>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet"
	href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
	integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
	crossorigin="anonymous">
<link rel="stylesheet"
	href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
<!-- Latest compiled and minified CSS -->
<link href="${contextPath}/resources/css/main.css" rel="stylesheet">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src='https://www.google.com/recaptcha/api.js'></script>
</head>


<body style="background: #e9ebf0">


	<div class="main-banner">
			<img src="${contextPath}/resources/images/IPT-Banner.jpg"
				class="img-responsive" alt="IPT Banner" style="width: 100%;">
	</div>

	<!-- Navbar -->
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="navbar-header">
				<a class="navbar-brand" href="/"><img
					src="${contextPath}/resources/images/IPT-Fut.svg"></a>
				<!--<a class="navbar-brand">Interactive Parallelization Tool</a> -->
			</div>

			<ul class="nav navbar-nav navbar-right">
				<c:if test="${pageContext.request.userPrincipal.name != null}">
						
						</form>
								Welcome ${pageContext.request.userPrincipal.name} | 
						<a
								href="${contextPath}/perform_logout"><span
						class="glyphicon glyphicon-log-out">Logout</span></a>
				</c:if>
			</ul>
		</div>
	</nav>
	

	<!--Tabs-->
	<div class="container">
		<ul class="nav nav-tabs">
			<c:if test="${pageContext.request.userPrincipal.name != null}">
			<li>&emsp;&emsp;&emsp;&nbsp;&nbsp;</li>
			<c:if test="${sessionScope.is_admin == 'true'}">
			<li id='admin-tab'><a href="${contextPath}/admin">Admin</a></li>
			</c:if>
			<li id='terminal-tab'><a href="${contextPath}/terminal">Terminal</a></li>
			
			<c:if test="${(sessionScope.is_admin == 'true')||(sessionScope.is_ldap == 'true')}">
			<li id='run-tab'><a href="${contextPath}/compileRun">Compile & Run</a></li>
			</c:if>
			<li id='history-tab'><a href="${contextPath}/jobHistory">Job
					History</a></li>
			<li id='help-tab' ><a data-toggle="dropdown" href="#" aria-expanded="false">Help
                <span class="caret"></span></a>
                <ul class="dropdown-menu" style="margin-left: -10px;margin-top: 0px">
                <li><a href="/faq">FAQ</a></li>
                <li><a href="/help">User Guide</a></li>
				<li><a href="/vdemos">Video Demos</a></li>
				<li><a href="/contactus">Contact Us</a></li>				
                </ul>
	</li>
			
			
			
			<li id='compile-tab'><a href="${contextPath}/comments">Message Board</a></li>
			<li id='aboutus-tab'><a href="${contextPath}/aboutus">About Us</a></li>
			</c:if>
			<c:if test="${pageContext.request.userPrincipal.name == null}">
			<li>&emsp;&emsp;&emsp;&nbsp;&nbsp;</li>

			<li id='help-tab' ><a data-toggle="dropdown" href="#" aria-expanded="false">Help
                <span class="caret"></span></a>
                <ul class="dropdown-menu" style="margin-left: -10px;margin-top: 0px">
                <li><a href="/faq">FAQ</a></li>
                <li><a href="/help">User Guide</a></li>
				<li><a href="/vdemos">Video Demos</a></li>
				<li><a href="/contactus">Contact Us</a></li>				
                </ul>
	</li>
			<li id='compile-tab'><a href="${contextPath}/comments">Message Board</a></li> 
			<li id='aboutus-tab'><a href="${contextPath}/aboutus">About Us</a></li>
			<li>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</li><li id="signup-tab"><a href="/registration" >Sign Up</a></li>
    <li id="login-tab" ><a href="/login_normal" >Log In</a>
	</li>
			</c:if>
		</ul>
		<!-- End Tabs -->

		<div class="tab-content">


		

		</div>
	</div>

		
	<script
		src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<script
		src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
		integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
		crossorigin="anonymous"></script>
	<!-- Latest compiled and minified JavaScript -->
	<script
		src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>


