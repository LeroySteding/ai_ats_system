import {
    Container,
    Heading,
  } from "@chakra-ui/react"
  import { createFileRoute } from "@tanstack/react-router"
  import { z } from "zod"

  import Navbar from "../../components/Common/Navbar"
  import AddApplication from "../../components/Admin/AddApplication"

  const applicationsSearchSchema = z.object({
    page: z.number().catch(1),
  })

  export const Route = createFileRoute("/_layout/ats")({
    component: ATS,
    validateSearch: (search) => applicationsSearchSchema.parse(search),
  })

//   const PER_PAGE = 5

//   function getApplicationsQueryOptions({ page }: { page: number }) {
//     return {
//       queryFn: () =>
//         ApplicationsService.readApplications({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
//       queryKey: ["applications", { page }],
//     }
//   }

//   function ApplicationsTable() {
//     const queryClient = useQueryClient()
//     const { page } = Route.useSearch()
//     const navigate = useNavigate({ from: Route.fullPath })
//     const setPage = (page: number) =>
//       navigate({ search: (prev) => ({ ...prev, page }) })

//     const {
//       data: applications,
//       isPending,
//       isPlaceholderData,
//     } = useQuery({
//       ...getApplicationsQueryOptions({ page }),
//       placeholderData: (prevData) => prevData,
//     })

//     const hasNextPage = !isPlaceholderData && applications?.data.length === PER_PAGE
//     const hasPreviousPage = page > 1

//     useEffect(() => {
//       if (hasNextPage) {
//         queryClient.prefetchQuery(getApplicationsQueryOptions({ page: page + 1 }))
//       }
//     }, [page, queryClient, hasNextPage])

//     return (
//       <>
//         <TableContainer>
//           <Table size={{ base: "sm", md: "md" }}>
//             <Thead>
//               <Tr>
//                 <Th>ID</Th>
//                 <Th>Applicant Name</Th>
//                 <Th>Job Title</Th>
//                 <Th>Status</Th>
//                 <Th>Actions</Th>
//               </Tr>
//             </Thead>
//             {isPending ? (
//               <Tbody>
//                 <Tr>
//                   {new Array(4).fill(null).map((_, index) => (
//                     <Td key={index}>
//                       <SkeletonText noOfLines={1} paddingBlock="16px" />
//                     </Td>
//                   ))}
//                 </Tr>
//               </Tbody>
//             ) : (
//               <Tbody>
//                 {applications?.data.map((application) => (
//                   <Tr key={application.id} opacity={isPlaceholderData ? 0.5 : 1}>
//                     <Td>{application.id}</Td>
//                     <Td isTruncated maxWidth="150px">
//                       {application.applicant_name}
//                     </Td>
//                     <Td
//                       color={!application.job_title ? "ui.dim" : "inherit"}
//                       isTruncated
//                       maxWidth="150px"
//                     >
//                       {application.job_title || "N/A"}
//                     </Td>
//                     <Td>{application.status}</Td>
//                     <Td>
//                       <ActionsMenu type={"Application"} value={application} />
//                     </Td>
//                   </Tr>
//                 ))}
//               </Tbody>
//             )}
//           </Table>
//         </TableContainer>
//         <Flex
//           gap={4}
//           alignItems="center"
//           mt={4}
//           direction="row"
//           justifyContent="flex-end"
//         >
//           <Button onClick={() => setPage(page - 1)} isDisabled={!hasPreviousPage}>
//             Previous
//           </Button>
//           <span>Page {page}</span>
//           <Button isDisabled={!hasNextPage} onClick={() => setPage(page + 1)}>
//             Next
//           </Button>
//         </Flex>
//       </>
//     )
//   }

  function ATS() {
    return (
      <Container maxW="full">
        <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
          Applications Management
        </Heading>

        <Navbar type={"Application"} addModalAs={AddApplication} />
        {/* <ApplicationsTable /> */}
      </Container>
    )
  }
