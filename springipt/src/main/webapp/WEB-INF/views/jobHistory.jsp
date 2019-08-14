<%@ page session="false"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib uri = "http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt"%>



<!DOCTYPE html>
<html lang="en">
<jsp:include page="base.jsp" />


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

		<h1>Job History</h1>

		<table class="table table-striped">
			<thead>
				<tr>
					<th>ID</th>
					<th>Type</th>
					<th>Status</th>
					<th>No. Nodes</th>
					<th>No. Cores</th>
					<th>Submission Date</th>
					<th>Start Date</th>
					<th>Date Received</th>
					<th>Execution Time(s)</th>
					<th>Error</th>
						
					
				</tr>
			</thead>
			


			<c:forEach var="job" items="${jobs}">
				<tr>
					
					<td>${job.id}</td>
					<td>${job.type}</td>
					<td>${job.status}</td>
					<td>${job.n_nodes}</td>
					<td>${job.n_cores}</td>
					<td>${job.date_submitted}</td>
					<td>${job.date_started}</td>
					<td>${job.date_server_received}</td>
					<td>${job.sc_execution_time}</td>
					<td>${job.error}</td>

					
				</tr>
			</c:forEach>
				
			
		</table>

	</div>

	<jsp:include page="footer.jsp" />

</body>
</html>