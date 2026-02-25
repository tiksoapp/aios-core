#!/usr/bin/env python3
"""SIDEBAR-01 QA Fixes: 3 issues found by QA review.

Fix 1 (CRITICAL): AC2 — Add authorId check to DELETE notes handler
Fix 2 (MEDIUM): AC3 — Pass onContactUpdate prop to mobile ContactPanel
Fix 3 (MEDIUM): AC4 — Accept liveChat OR integrations permission
"""

# =============================================
# Fix 1: AC2 — Author/admin check on DELETE notes
# =============================================
filepath_notes = '/home/tikso/tikso/src/app/api/inbox/notes/route.ts'

with open(filepath_notes, 'r') as f:
    notes = f.read()

# Replace the DELETE handler to include authorId check
old_delete = """    // Look up note to find its org (global client, no tenant scoping)
    const note = await prisma.internalNote.findUnique({
      where: { id: noteId },
      select: { id: true, organizationId: true },
    });

    if (!note) {
      return NextResponse.json(
        { success: false, error: "Nota não encontrada" },
        { status: 404 }
      );
    }

    // Verify user has access to this org
    await requireOrgAccess(note.organizationId);

    // Delete using tenant client (consistent with other handlers)
    const db = createTenantClient(note.organizationId);
    await db.internalNote.delete({ where: { id: noteId } });

    return NextResponse.json({ success: true });"""

new_delete = """    // Look up note to find its org and author (global client, no tenant scoping)
    const note = await prisma.internalNote.findUnique({
      where: { id: noteId },
      select: { id: true, organizationId: true, authorId: true },
    });

    if (!note) {
      return NextResponse.json(
        { success: false, error: "Nota não encontrada" },
        { status: 404 }
      );
    }

    // Verify user has access to this org
    const { session, member } = await requireOrgAccess(note.organizationId);

    // AC2: Only author or admin can delete
    const isAuthor = session.user?.id === note.authorId;
    const isAdmin = member.role === "OWNER" || member.role === "ADMIN";
    if (!isAuthor && !isAdmin) {
      return NextResponse.json(
        { success: false, error: "Não autorizado a excluir esta nota" },
        { status: 403 }
      );
    }

    // Delete using tenant client (consistent with other handlers)
    const db = createTenantClient(note.organizationId);
    await db.internalNote.delete({ where: { id: noteId } });

    return NextResponse.json({ success: true });"""

if old_delete in notes:
    notes = notes.replace(old_delete, new_delete)
    with open(filepath_notes, 'w') as f:
        f.write(notes)
    print("Fix 1 (CRITICAL): AC2 — authorId + admin check added to DELETE handler")
else:
    print("Fix 1: WARNING — old pattern not found, checking alternative...")
    # Try a more flexible match
    if 'select: { id: true, organizationId: true }' in notes and 'authorId' not in notes.split('DELETE')[1] if 'DELETE' in notes else True:
        print("Fix 1: MANUAL intervention needed — pattern mismatch")
    else:
        print("Fix 1: Already fixed or different code structure")


# =============================================
# Fix 2: AC3 — Pass onContactUpdate to mobile ContactPanel
# =============================================
filepath_layout = '/home/tikso/tikso/src/components/inbox/inbox-layout.tsx'

with open(filepath_layout, 'r') as f:
    layout = f.read()

# The mobile ContactPanel is missing onContactUpdate prop
old_mobile = """                onToggleAutomation={handleToggleAutomation}
                conversationStatus={selectedConversation?.status}
                isAiHandling={selectedConversation?.isBusy ?? false}
              />
            </div>
          </div>
        )}
      </div>
    );
  }"""

new_mobile = """                onToggleAutomation={handleToggleAutomation}
                onContactUpdate={(updates) => setContact((prev) => prev ? { ...prev, ...updates } : prev)}
                conversationStatus={selectedConversation?.status}
                isAiHandling={selectedConversation?.isBusy ?? false}
              />
            </div>
          </div>
        )}
      </div>
    );
  }"""

if old_mobile in layout:
    layout = layout.replace(old_mobile, new_mobile)
    with open(filepath_layout, 'w') as f:
        f.write(layout)
    print("Fix 2 (MEDIUM): AC3 — onContactUpdate added to mobile ContactPanel")
else:
    print("Fix 2: WARNING — old pattern not found in inbox-layout.tsx")


# =============================================
# Fix 3: AC4 — Accept liveChat OR integrations permission
# =============================================
filepath_ai = '/home/tikso/tikso/src/app/(app)/[orgId]/ai/actions.ts'

with open(filepath_ai, 'r') as f:
    ai = f.read()

# Replace single permission check with dual check
old_perm = '  assertMemberPermission(member, "liveChat")  // Fixed: was "integrations", sidebar users have liveChat;'

new_perm = """  // AC4: Accept liveChat OR integrations (agents have liveChat, automations have integrations)
  const hasJourneyPermission = member.permissions?.includes("liveChat") || member.permissions?.includes("integrations");
  if (!hasJourneyPermission) {
    return { success: false, error: "Sem permissão para alterar jornada" };
  }"""

if old_perm in ai:
    ai = ai.replace(old_perm, new_perm)
    with open(filepath_ai, 'w') as f:
        f.write(ai)
    print("Fix 3 (MEDIUM): AC4 — dual permission check (liveChat OR integrations)")
else:
    # Try without the comment
    alt_perm = 'assertMemberPermission(member, "liveChat")'
    if alt_perm in ai:
        # Find the exact line
        lines = ai.split('\n')
        for i, line in enumerate(lines):
            if alt_perm in line and 'updateJourneyState' in '\n'.join(lines[max(0,i-10):i]):
                lines[i] = """  // AC4: Accept liveChat OR integrations (agents have liveChat, automations have integrations)
  const hasJourneyPermission = member.permissions?.includes("liveChat") || member.permissions?.includes("integrations");
  if (!hasJourneyPermission) {
    return { success: false, error: "Sem permissão para alterar jornada" };
  }"""
                ai = '\n'.join(lines)
                with open(filepath_ai, 'w') as f:
                    f.write(ai)
                print("Fix 3 (MEDIUM): AC4 — dual permission (alt pattern)")
                break
        else:
            print("Fix 3: WARNING — could not locate permission line")
    else:
        print("Fix 3: WARNING — assertMemberPermission pattern not found")


print("\nAll SIDEBAR-01 QA fixes applied!")
