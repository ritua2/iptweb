<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:set var="contextPath" value="${pageContext.request.contextPath}"/>
<jsp:include page="base.jsp" />

<script src="${contextPath}/resources/js/bootstrap.min.js"></script>

<br />
<br />
<div class="container">
    <center>
        <h1>The link is not valid, your account has been deleted. Please create the account again</h1>
		
		
		
    </center>
</div>
<br/>
<br/>

<!-- /container -->
<jsp:include page="footer.jsp" />
<% 
 	session.invalidate(); 
	java.util.concurrent.TimeUnit.SECONDS.sleep(1);
 	response.sendRedirect("/springipt/");
 %>