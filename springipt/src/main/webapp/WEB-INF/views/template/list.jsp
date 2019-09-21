<%@ page session="false"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>

<c:set var="contextPath" value="${pageContext.request.contextPath}"/>
<jsp:include page="../base.jsp" />
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Comments</title>

    <!--<link href="${contextPath}/resources/css/bootstrap.min.css" rel="stylesheet">
    <link href="${contextPath}/resources/css/common.css" rel="stylesheet">-->

</head>
<body>

	<div class="container">

		<c:if test="${not empty msg}">
			<div class="alert alert-${css} alert-dismissible" role="alert">
				<button type="button" class="close" data-dismiss="alert"
					aria-label="Close">
					<span aria-hidden="true">&times;</span>
				</button>
				<strong>${msg}</strong>
			</div>
		</c:if>
		
		<c:if test="${pageContext.request.userPrincipal.name != null}">
		<button class="btn btn-primary"
							onclick="location.href='/springipt/template/addcomment'">Post Comment</button>
		<!--<h3>Click <a href="/springipt/template/addcomment">here</a> to post a comment</h3>-->
		</c:if>
		<table class="table table-striped">
			<thead>
				<tr>
					<th>#ID</th>
					<th>Title</th>
					<th>Body</th>
					<th>Tag</th>
				</tr>
			</thead>

			<c:forEach var="comment" items="${comments}">
				<tr>
					<td>${comment.id}</td>
					<td>${comment.title}</td>
					<td>${comment.body}</td>
					<td>${comment.tag}</td>

					<td><spring:url value="/comments/${comment.id}" var="userUrl" />
						<spring:url value="/comments/${comment.id}/update" var="updateUrl" />
						<spring:url value="/comments/${comment.id}/delete" var="deleteUrl" />
						<spring:url value="/comments/${comment.id}/reply" var="replyUrl" />

						<button class="btn btn-info" onclick="location.href='${userUrl}'">Details</button>
						<c:if test="${pageContext.request.userPrincipal.name != null}">
						<c:if test="${pageContext.request.userPrincipal.name == comment.createdby}">
						<button class="btn btn-primary"
							onclick="location.href='${updateUrl}'">Edit</button>
						<button class="btn btn-danger"
							onclick="this.disabled=true;location.href='${deleteUrl}'">Delete</button>
							</c:if>
						
						<button class="btn btn-success"
							onclick="this.disabled=true;location.href='${replyUrl}'">Reply</button>
						</c:if>
					</td>
				</tr>
				<c:forEach var="reply" items="${comment.replies}">
					<tr>
						<td></td>
						<td>${reply.title}</td>
						<td>${reply.body}</td>
						<td>${reply.tag}</td>
						<td></td>
					</tr>
				</c:forEach>
			</c:forEach>
		</table>

	</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="${contextPath}/resources/js/bootstrap.min.js"></script>
	

</body>
</html>
<jsp:include page="../footer.jsp" />