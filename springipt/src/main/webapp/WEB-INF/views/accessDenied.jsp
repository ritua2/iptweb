<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>

<c:set var="contextPath" value="${pageContext.request.contextPath}" />
<body>
<h2>Sorry, you do not have permission to view this page.</h2>
 
Click <a href="<c:url value="/" /> ">here</a>
to go back to the Homepage.
</body>