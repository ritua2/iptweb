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

    <title>Log in with your TACC account</title>

   <!--  <link href="${contextPath}/resources/css/bootstrap.min.css" rel="stylesheet">
    <link href="${contextPath}/resources/css/common.css" rel="stylesheet">-->

</head>

<body>

<div class="container">

<div class="col-sm-3 info">
                   
                    
                </div>

    <form method="POST" action="${contextPath}/login" class="form-signin"  style="width: 30%; margin-left: 400px">
        <h2 class="form-heading">Login as a TACC user.</h2>

        <div class="form-group ${error != null ? 'has-error' : ''}">
            <span>${message}</span>
			<span>${name}</span>
            <input name="username" type="text" class="form-control" placeholder="Username"
                   autofocus="true" style="margin-bottom:20px"/>
            <input name="password" type="password" class="form-control" placeholder="Password" style="margin-bottom:20px"/>
            <span>${error}</span>
            <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>

            <button class="btn btn-lg btn-primary btn-block" type="submit">Log In</button>
            
        </div>

    </form>

</div>
<jsp:include page="footer.jsp" />
<!-- /container -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="${contextPath}/resources/js/bootstrap.min.js"></script>
</body>
</html>
